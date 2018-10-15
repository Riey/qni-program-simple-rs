#include "./qni.h"
#include <thread>
#include <iostream>
#include <string>
#include <exception>

struct QniCollectedException : public std::exception
{
  char const *what() const throw()
  {
    return "Program is collected";
  }
};

inline void
qni_print_line_cpp(void *ctx, std::string &&text)
{
  if (qni_print_line(ctx, &text[0], text.length()) == -1)
  {
    throw QniCollectedException();
  }
}

void qni_entry(void *ctx)
{

  try
  {
    qni_set_back_color(ctx, 0xFF000000);
    qni_set_text_color(ctx, 0xFFFFFFFF);
    qni_set_highlight_color(ctx, 0xFFFFFF00);

    int32_t sum = 0;

    qni_print_line_cpp(ctx, "-1을 입력하면 종료합니다");

    while (true)
    {
      qni_print_line_cpp(ctx, "합계: " + std::to_string(sum));

      int32_t ret;
      qni_wait_int(ctx, &ret);

      if (ret == -1)
      {
        break;
      }

      sum += ret;
      qni_delete_line(ctx, 1);
    }
  }
  catch (std::exception const &e)
  {
    std::cerr << e.what() << std::endl;
  }
}

void start_program(void *hub)
{
  auto ret = qni_start_program(hub, u8"127.0.0.1:4434", sizeof(u8"127.0.0.1:4434") - 1);

  std::cout << "program exited code: " << ret << std::endl;
}

int main()
{
  qni_init_program();

  auto hub = qni_hub_new(qni_entry);

  auto thrd = std::thread(start_program, hub);

  std::string input;

  std::cout << "Input Q to exit..." << std::endl;

  while (true)
  {
    std::cin >> input;

    if (input == "Q")
    {
      break;
    }
  }

  qni_hub_exit(hub);

  std::cout << "Wait program exit..." << std::endl;

  thrd.join();

  qni_hub_delete(hub);

  return 0;
}
