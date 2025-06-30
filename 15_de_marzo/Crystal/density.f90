program density
implicit none
integer, parameter :: nhis=720
integer(8) :: i, j, m
integer :: ig, npart
integer, dimension(:), allocatable :: b
! CORRECCIÓN: Se eliminaron variables no usadas (b1,b2,b3,b4) y se añadió la nueva rho_r
real(8) :: bm,box,dx,hx,dy,hy,dz,hz,delr,r,rmin,rmax,rmed,hint,norm_factor, r_sq
real(8) :: pi = 3.14159265359
real(8), dimension(:), allocatable :: x,y,z
real(8), dimension(nhis) :: hist,hs1,hs2,base,rho_r
! character(32) :: a
character(2) :: ele
real, parameter :: r_cut = 720.0*sqrt(3.0) ! Distancia de corte en Angstroms
real, parameter :: r_cut_sq = r_cut**2


open(unit=10,file='shell.xyz')
read(10,*) npart
! read(10,*) a !uncomment for dump
allocate(b(npart))
allocate(x(npart))
allocate(y(npart))
allocate(z(npart))

bm = 0.0

do i=1,npart
   read(10,*) ele, x(i), y(i), z(i)
   if(ele.eq.'Ni'.or.ele.eq.'1') b(i)=28 
   if(ele.eq.'Pt'.or.ele.eq.'2') b(i)=78 
   if(ele.eq.'Co'.or.ele.eq.'3') b(i)=27
   if(ele.eq.'Pd') b(i) = 46
   bm = bm + b(i)
end do

bm = bm/npart ! Esto es <f> en la fórmula

! Comentando las impresiones de depuración para limpiar la salida
! print*, x(1), y(1), z(1),b(1),bm
! print*, x(2), y(2), z(2),b(2),bm
! print*, x(3), y(3), z(3),b(3),bm

20 format(a2,3f12.5)
close(10)

delr = 0.1
box = nhis*delr
hist(:) = 0.0

m = int(npart,8) * int(npart-1,8) / 2
rmin = 10.0
rmax = 0.0
rmed = 0.0
hint = 0.0

!-----------------------------------------------------------------------
! PASO 1: BUCLE DE SUMATORIA
! Aquí solo acumulamos la suma ponderada de pares en cada bin del histograma.
!-----------------------------------------------------------------------
do i = 1, npart-1
   do j = i+1, npart
      dx = x(i) - x(j)
      dy = y(i) - y(j)
      dz = z(i) - z(j)
      r_sq = dx**2 + dy**2 + dz**2

      hx = dx - box * nint(dx / box)
      hy = dy - box * nint(dy / box)
      hz = dz - box * nint(dz / box)
      r = sqrt(hx**2 + hy**2 + hz**2)
      
      if (r < box) then
         ig = int(r/delr) + 1
         if (ig > 0 .and. ig <= nhis) then
            hist(ig) = hist(ig) + 2.0 * b(i) * b(j)
            rmed = rmed + r
            if (r < rmin) rmin = r
            if (r > rmax) rmax = r
         endif
      endif
   end do
end do

rmed = rmed/m

!-----------------------------------------------------------------------
! PASO 2: NORMALIZACIÓN
! Ahora normalizamos cada bin del histograma según la fórmula.
!-----------------------------------------------------------------------
rho_r(:) = 0.0
do i = 1,nhis
   ! Usamos el punto medio del bin para calcular r
   r = (real(i) - 0.5) * delr 
   if (r > 1e-6) then ! Evitar división por cero en el primer bin
      ! CORRECCIÓN: Este es el factor de normalización correcto.
      ! Denominador = N * <f>² * (Volumen de la cáscara esférica)
      ! Volumen de la cáscara = 4 * pi * r^2 * delr
      norm_factor = npart * bm**2 * (4.0 * pi * r**2 * delr)
      if (norm_factor > 1e-9) then
         rho_r(i) = hist(i) / norm_factor
      endif
   endif
end do

!-----------------------------------------------------------------------
! PASO 3: SUAVIZADO Y ESCRITURA (usando los resultados correctos)
!-----------------------------------------------------------------------
! Aplicando suavizado para obtener una distribución más continua. Ahora se aplica a rho_r.
call smooth(rho_r,2,hs1)
call smooth(rho_r,50,hs2)
call smooth(hs2,50,base)

! La densidad final suavizada es la señal menos la base de fondo
! CORRECCIÓN: la variable `dens` ahora tiene un significado físico claro.
! dens = hs1 - base

print*, npart,' atomos ',m,' pares '
print*, 'Rango de distancias ',rmin,'-',rmax
print*, 'Distancia promedio ',rmed

open(unit=11,file='density.txt',action='write',status='replace')
write(11,*) '#r(A)        ρ(r)_raw       ρ_smooth(r)         Base'
do i = 1,nhis
   r = (real(i) - 0.5) * delr
   write(11,30) r, rho_r(i), hs1(i), base(i)
end do
30 format(f10.4,3f15.7)
close(11)

contains

subroutine smooth(h,ns,f)
implicit none
integer, parameter :: nhis=720
integer :: i,j,ns,k
real(8) :: x, count
real(8),dimension(nhis) :: h,f

k = int(ns/2)
do i = 1,nhis
   x = 0.0
   count = 0.0 ! CORRECCIÓN: Es mejor contar los puntos reales sumados para promediar
   do j = i-k,i+k
      if (j>=1 .and. j<=nhis) then
         x = x + h(j)
         count = count + 1.0
      endif
   end do
   if (count > 0) then
      f(i) = x / count
   else
      f(i) = 0.0
   endif
end do

end subroutine

end program density