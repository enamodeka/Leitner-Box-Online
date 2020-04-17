from functools import wraps
# from sqlalchemy import create_engine, insert

def test_decorator(func):
  @wraps(func)
  def wrap_func(*args, **kwargs):
    func(*args, **kwargs)
    print('TEST DECORATOR PLEASE!!')
    return func(*args, **kwargs)
  return wrap_func


