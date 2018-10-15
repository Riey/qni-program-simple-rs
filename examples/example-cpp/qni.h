#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C"
{
#endif

  typedef void (*qni_program_entry_t)(void *ctx);

  void *qni_hub_new(qni_program_entry_t entry);
  void qni_hub_delete(void *hub);
  void qni_hub_exit(void *hub);

  int qni_print(void *ctx, char const *text, size_t len);
  int qni_print_line(void *ctx, char const *text, size_t len);
  int qni_new_line(void *ctx);
  int qni_delete_line(void *ctx, uint32_t count);

  int qni_set_font(void *ctx, char const *font_family, size_t font_family_len, float font_size, uint32_t font_style);
  int qni_set_text_align(void *ctx, uint32_t text_align);

  int qni_set_text_color(void *ctx, uint32_t color);
  int qni_set_back_color(void *ctx, uint32_t color);
  int qni_set_highlight_color(void *ctx, uint32_t color);

  int qni_wait_int(void *ctx, int32_t *ret);

  void qni_init_program();
  int qni_start_program(void *hub, char const *host, size_t host_len);

#ifdef __cplusplus
}
#endif
