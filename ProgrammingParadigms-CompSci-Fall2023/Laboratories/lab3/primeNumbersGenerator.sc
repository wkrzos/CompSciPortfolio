val primes = (toN: Int) => {
  def findPrimes(sieve: List[Int]): List[Int] =
    sieve match {
      case h :: t => h :: findPrimes(t.filter(x => x % h != 0))
      case Nil    => Nil
    }

  findPrimes(List.range(2, toN))
}

primes(1000)
