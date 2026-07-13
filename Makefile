CC      = gcc
CFLAGS  = -fPIC -shared -Ibackend/include

ifeq ($(DEBUG),1)
CFLAGS += -DDEBUG -g
endif

SRC_DIR = backend/src

SRCS = $(wildcard $(SRC_DIR)/*.c)

TARGET = $(SRC_DIR)/libtrie.so

# ── Default target ────────────────────────────────────────────────
all: $(TARGET)

# ── Link ──────────────────────────────────────────────────────────
$(TARGET): $(SRCS)
	$(CC) $(CFLAGS) $^ -o $@

.PHONY: clean

# ── Clean ─────────────────────────────────────────────────────────
clean:
	rm -f backend/src/libtrie.so