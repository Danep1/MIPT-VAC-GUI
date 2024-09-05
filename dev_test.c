#include <stdio.h>
#include <string.h>
#include <stdio.h>
#include <errno.h>
#include <fcntl.h>

#define HT_TMC "/dev/usbtmc1"
#define BUFLEN 62000

int usbtmc_write(int dev, const char *cmd)
{
	int r;

	r = write(dev, cmd, strlen(cmd));
	if (r == -1)
	{
		fprintf(stderr, "# E: unable to write to rs (%s)\n", strerror(errno));
	}

	return r;
}

int usbtmc_read(int dev, char *buf, int buf_length)
{
	int r;

	r = read(dev, buf, buf_length);
	if (r == -1)
	{
		fprintf(stderr, "# E: unable to read from rs (%s)\n", strerror(errno));
	}

	return r;
}

int main(int argc, char const *argv[])
{
	int r;

	int buflen = BUFLEN;
	char buf[BUFLEN] = {0};
	float *fbuf;
	int fbuf_index = 0;

	setlinebuf(stderr);

	r = open(HT_TMC, O_RDWR);
	if(r == -1)
	{
		fprintf(stderr, "# E: Unable to open rs (%s)\n", strerror(errno));
		return 1;
	}
	int osc_fd = r;

	usbtmc_write(osc_fd, "*IDN?"); 
	usbtmc_read(osc_fd, buf, buflen); 
	fprintf(stderr, "%s\n", buf); 
	memset(buf, 0, 100);
}