project(example_cpp)

add_executable(example main.cc)

target_link_libraries(example
    ${CMAKE_SOURCE_DIR}/../../target/debug/libqni_program_simple.so
    pthread)
