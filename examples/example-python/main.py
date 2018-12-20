import threading
import qni_binding
import sys
import os
import signal

qni_lib_path = '../../target/debug/libqni_program_simple.so'

if len(sys.argv) > 1:
    qni_lib_path = sys.argv[1]


QNI = qni_binding.QniBinding(qni_lib_path)
QNI.program_init()


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

    finally:
        os.kill(os.getpid(), signal.SIGINT)


def start_connector(hub):
    return QNI.connector_ws_start(hub, "127.0.0.1:4434")


ctx = QNI.console_new()

signal.signal(signal.SIGINT, lambda signum, frame: QNI.console_exit(ctx))

connector_thrd = threading.Thread(
    target=start_connector, args=[ctx]
)

connector_thrd.start()

game_thrd = threading.Thread(
    target=entry, args=[ctx]
)

game_thrd.start()

try:
    while True:
        user_input = input('Input Q to exit...\n')

        if user_input is 'Q':
            os.kill(os.getpid(), signal.SIGINT)
            break
except KeyboardInterrupt:
    pass

print('Wait for connector exit ...')

connector_thrd.join()

print('Wait for game exit ...')

game_thrd.join()

QNI.console_delete(ctx)
