program calcular_rdf
implicit none

! --- PARÁMETROS DE ANÁLISIS ---
integer, parameter :: nhis=650     ! Número de bins en el histograma
real(8), parameter  :: delr=0.05     ! Ancho de cada bin en Angstroms

! --- VARIABLES ---
integer(8) :: i, j
integer :: ig, npart
integer, dimension(:), allocatable :: tipo_atomo
real(8) :: L, L_half, r_max, l_max          ! L: Longitud de la caja, L_half: L/2, r_max: Distancia máxima de corte, distancial real máxima del cubo
real(8) :: dx, dy, dz, r_sq, r
real(8) :: rho_promedio              ! Densidad numérica promedio (N/V)
real(8) :: vol_shell, n_ideal                ! Volumen de la capa esférica y número ideal de partículas
real(8) :: pi = 3.14159265359
real(8), dimension(:), allocatable :: x, y, z
real(8), dimension(nhis) :: hist_g_r, g_r_raw, g_r_smooth, hs1, base, n_real
character(2) :: ele

! =======================================================================
! PASO 1: LEER DATOS Y OBTENER PARÁMETROS FUNDAMENTALES
! =======================================================================

! --- Leer el archivo de coordenadas ---
open(unit=10, file='shell.xyz', status='old', action='read')
read(10,*) npart
! Omitir la línea de comentario en el formato xyz estándar
read(10,*)

! --- Asignar memoria para las coordenadas y tipos ---
allocate(tipo_atomo(npart))
allocate(x(npart))
allocate(y(npart))
allocate(z(npart))

l_max = 0.0
! --- Leer las posiciones de los átomos ---
do i = 1, npart
   ! Asumimos un formato XYZ estándar: Elemento X Y Z
   read(10,*) ele, x(i), y(i), z(i)
   l_max = max(l_max, max(x(i), max(y(i), z(i))))
   ! Podrías usar 'tipo_atomo' si necesitas g(r) parciales (p.ej. Ni-Pt)
   ! Por ahora, no lo usaremos en el cálculo principal.
end do
close(10)

print *, "Leidos ", npart, " átomos del archivo shell.xyz"

! --- CORRECCIÓN CRÍTICA: OBTENER EL TAMAÑO DE LA CAJA ---
! La longitud de la caja 'L' NO se puede derivar de los parámetros del histograma.
! Debe ser la longitud de la caja cúbica usada en la simulación de DM.
print *, "======================================================"
! print *, "IMPORTANTE: Introduce la longitud de la caja cúbica (L) en Angstroms:"
L = nint(2.0 * l_max)  ! Asumimos que la caja es al menos el doble del máximo de las coordenadas
print *, "Usando L = ", L, " Angstroms para el cálculo de PBC."
print *, "======================================================"

! --- Calcular valores derivados ---
L_half = L / 2.0
r_max = L_half  ! No tiene sentido físico calcular g(r) más allá de L/2
if (r_max > real(nhis)*delr) then
    print *, "Advertencia: r_max (L/2) es mayor que el rango del histograma."
    print *, "El histograma cubrira hasta ", real(nhis)*delr
endif
rho_promedio = real(npart) / (L**3)

! --- Inicializar histograma ---
hist_g_r = 0.0

! =======================================================================
! PASO 2: CALCULAR EL HISTOGRAMA DE PARES (Conteo simple)
! =======================================================================

print *, "Calculando pares... (esto puede tardar un momento)"
do i = 1, npart - 1
   do j = i + 1, npart
      dx = x(i) - x(j)
      dy = y(i) - y(j)
      dz = z(i) - z(j)

      ! --- APLICAR CONDICIONES DE FRONTERA PERIÓDICAS (PBC) ---
      ! Esta es la Convención de la Imagen Mínima (MIC)
      dx = dx - L * nint(dx / L)
      dy = dy - L * nint(dy / L)
      dz = dz - L * nint(dz / L)

      r_sq = dx**2 + dy**2 + dz**2

      ! --- Llenar el histograma ---
      if (r_sq < r_max**2) then
         r = sqrt(r_sq)
         ig = int(r / delr) + 1
         if (ig <= nhis) then
            ! Contamos cada par dos veces (i viendo a j, y j viendo a i)
            hist_g_r(ig) = hist_g_r(ig) + 2.0
         endif
      endif
   end do
end do

! =======================================================================
! PASO 3: NORMALIZAR EL HISTOGRAMA PARA OBTENER g(r)
! =======================================================================
! g(r) = (Densidad local en r) / (Densidad promedio)
! g(r) = [N(r) / V_shell(r)] / rho_promedio
! Donde N(r) es el número promedio de partículas en la capa esférica a distancia r
! y V_shell(r) es el volumen de esa capa.

g_r_raw(:) = 0.0
do i = 1, nhis
   r = (real(i) - 0.5) * delr  ! Radio en el punto medio del bin
   if (r > 1e-9) then
      ! Volumen de la capa esférica de radio r y grosor delr
      ! V_shell = 4/3 * pi * ((r+delr/2)^3 - (r-delr/2)^3) ~= 4 * pi * r^2 * delr
      vol_shell = 4.0 * pi * r**2 * delr

      ! Número ideal de partículas en la capa para un gas uniforme
      n_ideal = rho_promedio * vol_shell

      ! Número promedio de partículas encontradas en la simulación
      ! El histograma contiene la suma sobre TODOS los N*(N-1)/2 pares.
      ! Para obtener el promedio por partícula de referencia, dividimos por N.
      n_real(i) = hist_g_r(i) / real(npart)

      ! Calcular g(r)
      if (n_ideal > 1e-9) then
         g_r_raw(i) = n_real(i) / n_ideal
      endif
   endif
end do

! =======================================================================
! PASO 4: SUAVIZADO Y ESCRITURA DE RESULTADOS
! =======================================================================

! Aplicando un suavizado simple (promedio móvil) a la g(r) calculada

print*, "Densidad promedio: ", rho_promedio

call smooth(g_r_raw, 5, g_r_smooth)
call smooth(g_r_raw, 50, hs1)
call smooth(hs1, 50, base)

print *, "Cálculo completo. Escribiendo resultados en rdf.txt"
open(unit=11, file='rdf.txt', action='write', status='replace')
write(11, '(A)') '#r(A)          g(r)_raw       g(r)_smooth       Base'
do i = 1, nhis
   r = (real(i) - 0.5) * delr
   if (r > r_max) cycle ! No escribimos datos más allá de L/2
   write(11, 30) r, g_r_raw(i), g_r_smooth(i), base(i)
end do
30 format(f10.4,3f15.7)
close(11)

contains

! --- SUBRUTINA DE SUAVIZADO (PROMEDIO MÓVIL) ---
subroutine smooth(h_in, ns, f_out)
    implicit none
    integer, intent(in) :: ns
    real(8), dimension(:), intent(in) :: h_in
    real(8), dimension(:), intent(out) :: f_out
    
    integer :: i, j, k, n, count
    real(8) :: total
    
    n = size(h_in)
    k = ns / 2
    f_out = 0.0
    
    do i = 1, n
        total = 0.0
        count = 0
        do j = i - k, i + k
            if (j >= 1 .and. j <= n) then
                total = total + h_in(j)
                count = count + 1
            endif
        end do
        if (count > 0) then
            f_out(i) = total / real(count)
        endif
    end do
end subroutine

end program calcular_rdf