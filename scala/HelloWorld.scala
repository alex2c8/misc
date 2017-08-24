object HelloWorld {

	def sum(xs: List[Int]): Int = {
		xs match {
			case Nil => 0
			case x :: xs => x + sum(xs)
		}
	}

	def main(args: Array[String]) {
		val list = List(1, 2, 3, 4, 5)
		println(sum(list))
   }
}