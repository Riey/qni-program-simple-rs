#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C"
{
#endif

  enum QNI_WAIT_RESULT
  {
    QNI_WAIT_OK = 0,
    QNI_WAIT_TIMEOUT = 1,
    QNI_WAIT_EXITED = -1,
  };

  void *qni_console_new();
  void qni_console_delete(void *ctx);
  void qni_console_exit(void *ctx);

  void qni_print(void *ctx, char const *text, size_t len);
  void qni_print_line(void *ctx, char const *text, size_t len);
  void qni_draw_line(void *ctx);
  void qni_new_line(void *ctx);
  void qni_delete_line(void *ctx, uint32_t count);

  void qni_set_font(void *ctx, char const *font_family, size_t font_family_len, float font_size, uint32_t font_style);
  void qni_set_text_align(void *ctx, uint32_t text_align);

  void qni_set_text_color(void *ctx, uint32_t color);
  void qni_set_back_color(void *ctx, uint32_t color);
  void qni_set_highlight_color(void *ctx, uint32_t color);

  void qni_str_delete(uint8_t* ptr, size_t len, size_t cap);

  QNI_WAIT_RESULT qni_wait_int(void *ctx, int32_t *ret);
  QNI_WAIT_RESULT qni_wait_str(void *ctx, uint8_t **ret, size_t* ret_len, size_t* ret_cap);

  void qni_program_init();
  int32_t qni_program_start(void *ctx, char const *host, size_t host_len);

#ifdef __cplusplus
}
#endif
