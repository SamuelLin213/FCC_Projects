class Rectangle:
  width = 0
  height = 0
  
  def __init__(self, width, height):
    self.width = width
    self.height = height
  def set_width(self, width):
    self.width = width
  def set_height(self, height):
    self.height = height
  def get_area(self):
    return self.height * self.width
  def get_perimeter(self):
    return (2 * self.width + 2 * self.height)
  def get_diagonal(self):
    return ((self.width ** 2 + self.height ** 2) ** 0.5)
  def get_picture(self):
    if(self.width > 50 or self.height > 50):
      return "Too big for picture."

    shape = ""

    for y in range(self.height):
      for x in range(self.width):
        shape += "*"
      shape += "\n"

    return shape

  def __str__(self):
    return "Rectangle(width=" + str(self.width) + ", height=" + str(self.height) + ")"

  def get_amount_inside(self, shape):
    return self.get_area() // shape.get_area()
  
class Square(Rectangle):
  
  def __init__(self, side):
    super().__init__(side, side)
  def set_side(self, side):
    self.height = side
    self.width = side
  def __str__(self):
    return "Square(side=" + str(self.height) + ")"
  def set_width(self, side):
    self.width = side
    self.height = side
  def set_height(self, side):
    self.height = side
    self.width = side
  
    