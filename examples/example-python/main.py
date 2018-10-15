import threading
import qni_binding

QNI = qni_binding.QniBinding('../../target/debug/libqni_program_simple.so')

QNI.init_program()


def entry(ctx):

    try:

        QNI.set_back_color(ctx, 0x00000000)
        QNI.set_text_color(ctx, 0xFFFFFFFF)
        QNI.print_line(ctx, "-1을 입력하면 종료합니다")

        total = 0

        while True:
            QNI.print_line(ctx, "합계: %d" % total)

            ret = QNI.wait_int(ctx)

            print("입력: %d" % ret)

            if ret is -1:
                print("종료합니다")
                break

            QNI.delete_line(ctx, 1)
            total += ret

    except qni_binding.QniEndError:
        return


def start_connector(hub):
    return QNI.connector_ws_start(hub, "127.0.0.1:4434")


hub = QNI.hub_new(qni_binding.QNI_ENTRY_CALLBACK(entry))

connector_thrd = threading.Thread(
    target=start_connector, args=[hub])

connector_thrd.start()

while True:
    user_input = input('Input Q to exit...\n')

    if user_input is 'Q':
        break

QNI.hub_exit(hub)

print('Wait for connector exit...')

connector_thrd.join()

QNI.hub_delete(hub)
