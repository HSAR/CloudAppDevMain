/* Adapted from Chris Ackerman's node module
 * (https://github.com/ChrisAckerman/adler32) - ported to standard JS, make it
 * use strings instead of arrays of bytes. UTF-8 string desirable. */
/* Lines with comments marked MWRC have been modified from the original */
/* MWRC Remove node-specific shebang line and "use strict" */

/**
 * Largest prime smaller than 2^16 (65536)
 */
var BASE = 65521;

/**
 * Largest value n such that 255n(n+1)/2 + (n+1)(BASE-1) <= 2^32-1
 *
 * NMAX is just how often modulo needs to be taken of the two checksum word halves to prevent overflowing a 32 bit
 * integer. This is an optimization. We "could" take the modulo after each byte, and it must be taken before each
 * digest.
 */
var NMAX = 5552;

function sum(buf, adler) /* MWRC convert from node to generic JS */
{
	if (adler == null)
		adler = 1;

	var a = adler & 0xFFFF,
		b = (adler >>> 16) & 0xFFFF,
		i = 0,
		max = buf.length,
		n, value;

	while (i < max)
	{
		n = Math.min(NMAX, max - i);

		do
		{
			a += buf.charCodeAt(i++)<<0; /* MWRC use string not byte array */
			b += a;
		}
		while (--n);

		a %= BASE;
		b %= BASE;
	}

	return ((b << 16) | a) >>> 0;
} /* MWRC convert from node to generic JS */

function roll(sum, length, oldByte, newByte) /* MWRC convert from node to generic JS */
{
	var a = sum & 0xFFFF,
		b = (sum >>> 16) & 0xFFFF;

	if (newByte != null)
	{
		a = (a - oldByte + newByte + BASE) % BASE;
		b = (b - ((length * oldByte) % BASE) + a - 1 + BASE) % BASE;
	}
	else
	{
		a = (a - oldByte + BASE) % BASE;
		b = (b - ((length * oldByte) % BASE) - 1 + BASE) % BASE;
	}

	return ((b << 16) | a) >>> 0;
} /* MWRC convert from node to generic JS */
