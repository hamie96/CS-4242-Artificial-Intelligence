require 'ruby2d'

set background: 'white'

x = 200
circle1 = Circle.new(
	x : x, y: 175,
	radius: 30,
	sectors: 32,
	color: 'blue',
	z:10
)
update do
circle1(x:x)	


	x+=1
end

show
