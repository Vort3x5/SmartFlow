#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/i2c-dev.h>
#include <stdint.h>

int main() {
    int file;
    if ((file = open("/dev/i2c-1", O_RDWR)) < 0) exit(1);
    if (ioctl(file, I2C_SLAVE, 0x48) < 0) exit(1);

    uint8_t config[3] = {0x01, 0xC3, 0x83};
    uint8_t reg[1] = {0x00};
    uint8_t data[2] = {0};

    if (write(file, config, 3) != 3) exit(1);
    usleep(15000);
    if (write(file, reg, 1) != 1 || read(file, data, 2) != 2) exit(1);

    int16_t val = (data[0] << 8) | data[1];
    float voltage = val * 4.096 / 32767.0;

    float max_v = 2.460;
    float min_v = 1.624;
    float percent = ((max_v - voltage) / (max_v - min_v)) * 100.0;

    if (percent < 0.0) percent = 0.0;
    if (percent > 100.0) percent = 100.0;

    printf("%.1f\n", percent);

    close(file);
    return 0;
}
