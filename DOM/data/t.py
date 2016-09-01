# encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


s = '''

<pre id="best-content-2489572061" accuse="aContent" class="best-text mb-10" style="min-height: 55px;">电影原声带专辑：《One Day (Original Motion Picture Soundtrack)》<br>发行时间：	2011年08月16日<br>专辑收录了电影中的插曲曲目：<br>01	Sparkling Day-- Elvis Costello<br>	02	Roll to Me-- Del Amitri<br>	03	Aftermath (Hip Hop Blues) --Tricky<br>	04	Reverend Black Grape-- Black Grape<br>	05	Born of Frustration --James<br>	06	Rocks-- Primal Scream<br>	07	Praise You (One Day OST Version)-- Fatboy Slim<br>	08	The Rhythm of the Night-- Corona<br>	09	Angels --Robbie Williams<br>	10	Life Is a Rollercoaster-- Ronan Keating<br>	11	Sowing the Seeds of Love ---Tears for Fears <br>	12	Joy --François Feldman <br>	13	Tear Off Your Own Head (It's a Doll Revolution) ---Elvis Costello<br>	14	One Day Main Titles --Rachel Portman<br>	15	Wedding Chorus --Rachel Portman<br>	16	July 15Th --Rachel Portman<br>	17	We Had Today --Rachel Portman</pre>

'''

print "".join([x.strip() for x in s.strip().split("\n")]).replace("\t", "")

