def root3(a: Float): Float =
  def e = 1e-15

  if a < 0.0 then
    Float.NaN
  else if a == 0.0 then
    0.0
  else
    def root3Helper(x: Float): Float =
      if (x * x * x - a).abs <= e * a.abs then
        x
      else
        val next_x = x + (a / (x * x) - x) / 3
        root3Helper(next_x)

    root3Helper(a)

root3(0.0)
root3(8.0)
root3(125.0)
