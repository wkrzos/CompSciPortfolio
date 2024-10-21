class RefCounter
{
public:
  RefCounter();
  int add() { return ++refCount; };
  int dec() { return --refCount; };
  int get() { return refCount; };

private:
  int refCount;
};

RefCounter::RefCounter() : refCount(0)
{
	// No logic needed (?)
}