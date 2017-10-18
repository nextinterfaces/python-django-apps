#!/usr/bin/env python
import sys
import nextinterfaces.main
import nextinterfaces.types
import nextinterfaces.objects

if __name__ == '__main__':
    m = nextinterfaces.objects.molecule()
    print m
    sys.exit(nextinterfaces.main.main())
