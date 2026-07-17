CC      = gcc
CFLAGS  = -fPIC -shared -Ibackend/include
TEST_CFLAGS = -Ibackend/include

ifeq ($(DEBUG),1)
CFLAGS += -DDEBUG -g
TEST_CFLAGS += -DDEBUG -g
endif

SRC_DIR = backend/src
TEST_DIR = backend/tests

SRCS = $(wildcard $(SRC_DIR)/*.c)
TEST_SRCS = $(TEST_DIR)/test_trie.c $(SRC_DIR)/trie.c

TARGET = $(SRC_DIR)/libtrie.so
TEST_TARGET = $(TEST_DIR)/test_trie

# ── Default target ────────────────────────────────────────────────
all: $(TARGET)

# ── Test target ─────────────────────────────────────────────────────
test: $(TEST_TARGET)
	./$(TEST_TARGET)

# ── Link ──────────────────────────────────────────────────────────
$(TARGET): $(SRCS)
	$(CC) $(CFLAGS) $^ -o $@

$(TEST_TARGET): $(TEST_SRCS)
	$(CC) $(TEST_CFLAGS) $^ -o $@

.PHONY: clean test

# ── Clean ─────────────────────────────────────────────────────────
clean:
	rm -f backend/src/libtrie.so $(TEST_TARGET)