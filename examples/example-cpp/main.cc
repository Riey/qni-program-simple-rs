#include "./qni.h"
#include <thread>
#include <iostream>
#include <string>
#include <exception>

inline void
qni_print_line_cpp(void *ctx, std::string &&text)
{
  qni_print_line(ctx, &text[0], text.length());
}

void qni_entry(void *ctx)
{
  qni_set_back_color(ctx, 0xFF000000);
  qni_set_text_color(ctx, 0xFFFFFFFF);
  qni_set_highlight_color(ctx, 0xFFFFFF00);

  int32_t sum = 0;

  qni_print_line_cpp(ctx, "-1을 입력하면 종료합니다");
  qni_draw_line(ctx);

  while (true)
  {
    qni_print_line_cpp(ctx, "합계: " + std::to_string(sum));

    int32_t ret;
    if (qni_wait_int(ctx, &ret) != QNI_WAIT_OK)
    {
      break;
    }

    if (ret == -1)
    {
      break;
    }

    sum += ret;
    qni_delete_line(ctx, 1);
  }

  qni_console_exit(ctx);
}

void start_program(void *ctx)
{
  auto ret = qni_program_start(ctx, u8"127.0.0.1:4434", sizeof(u8"127.0.0.1:4434") - 1);

  std::cout << "program exited code: " << ret << std::endl;
}

int main()
{
  qni_program_init();

  auto ctx = qni_console_new();

  auto thrd = std::thread(start_program, ctx);
  auto game_thrd = std::thread(qni_entry, ctx);

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

  qni_console_exit(ctx);

  std::cout << "Wait program exit..." << std::endl;

  thrd.join();

  std::cout << "Wait game exit..." << std::endl;

  game_thrd.join();

  qni_console_delete(ctx);

  return 0;
}
