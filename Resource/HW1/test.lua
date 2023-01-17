

function st(a)
  a = "b"
  return a end
  
function stb(a)
  print(st(a))
  print(a)
  return a end
  
  
a = "hello"
stb(a)
