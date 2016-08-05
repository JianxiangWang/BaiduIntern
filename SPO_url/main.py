import sys

from ba import hadoop_main as ba
from shipin import hadoop_main as shipi

ba.main(sys.stdin)
shipi.main(sys.stdin)
