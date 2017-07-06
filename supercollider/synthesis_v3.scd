Server.default=s=Server.local;
s.boot;
//"https://github.com/supercollider/supercollider/wiki/Recording-in-SuperCollider-(WIP)" ... BuffWr or RecordBuff

( // (WIP) load .csv data
var biota, toyinput;
biota = asFloat(CSVFileReader.read("/Users/alexandriaguo/Documents/2016-2017/*misc/EMW/test code/scdInput.csv", true).postcs);
biota = biota.flop;
toyinput = [0.0174,0.0190,0.0290,0.0088,0.0083];
//the average is ~0.0165, reciprocal ~60
)

( // load .csv data (currently manually entered) into Array
  // NOTES: alternatively, try Pxrand, Pwalk; implement .csv loading
~dens = [0.0160, 0.0143, 0.00877];
~diam = Array.new;
~diam = ~diam.add(Pseq([
	Pshuf([53.5, 25.5, 21.5, 65, 24.5, 63], 1)], //253
inf));
~diam = ~diam.add(Pseq([
	Pshuf([36.5, 32, 28.5, 91], 1)],
inf));
~diam = ~diam.add(Pseq([
	Pshuf([33, 25.5, 25, 35, 33, 22, 21.5, 13, 21, 28], 1)],
inf));
)

( // load Buffers into Array
Buffer.freeAll;
~funk = Array.new;
~folder = PathName.new("/Applications/SuperCollider.app/Contents/Resources/sounds/funk/");

(~folder.entries.do{
	arg path;
	~funk = ~funk.add(Buffer.read(s, path.fullPath));
})
)

( // write single grain SynthDef
// e = Env(
// 	[0.2, 1.0, 0.7, 0.0], // x-levels
// 	[0.01, 0.5, 0.49], // y-intervals
// [3, -12, 3]).plot; // curvature;
e = Env([0, 1, 0], [0.01, 1], -4);

SynthDef(\bfgrain, {
	arg gdur=0.02, buf=0, rate=1, spos=0, pan=0, amp=0.5, out=0, dens;//, modfreq;
	var trig, sig, mod, env;
	trig = Impulse.ar(dens);
	env = EnvGen.kr(e, timeScale:gdur, doneAction:2);
	//mod = FSinOsc.ar(modfreq, 0, 1); // frequency modulation
	sig = PlayBuf.ar(2, buf, BufRateScale.kr(buf)*rate, trig, startPos:spos, loop:0);
	sig = sig * env; //*mod;
	sig = Pan2.ar(sig,pan,amp);
	Out.ar(out, sig);
}).add;
)

( // collect Pbinds into Array
~pbinds = Array.new;
3.do{ | i |
	~pbinds = ~pbinds.add(
		Pbind(
			\instrument, 'bfgrain',
			\dur, ~dens[i] * 100,
			\gdur, ~dens[i] * 100,
			\buf, ~funk[i].bufnum,
			\spos, Pseg(Pseq([0, ~funk[i].numFrames],inf), Pseq([~funk[i].duration,0],inf), \lin),
			\dens, ~dens[i] * 10000,
			\rate, ~diam[i] / 10,
		)
)};
)

~pbinds[0].play;
~pbinds[1].play;
~pbinds[2].play;

( // play Pbinds in parallel
TempoClock.default.tempo = 1;
//symphony:
Ptpar([0.0, ~pbinds[0], 2.0, ~pbinds[1], 4.0, ~pbinds[2], 6.0, ~pbinds[3], 8.0, ~pbinds[4]]).play;
)


//Testing
/*Synth(\bfgrain, [\dur, ~dens[1], \buf, ~funk[1].bufnum, \spos, 10002]);
{PlayBuf.ar(2, ~funk[1].bufnum, BufRateScale.kr(~funk[1].bufnum)*1, loop:1)}.play;*/
// bp1 = Pbind(
// 	\instrument, 'bfgrain',
// 	//\freq, ~col1,
// 	\dur, ~dens[1] * 100,
// 	\gdur, ~dens[1] * 100,
// 	\buf, ~funk[1].bufnum,
// 	\spos, Pseg(Pseq([0, ~funk[1].numFrames],inf), Pseq([~funk[1].duration,0],inf), \lin),
// 	\amp, 1,
// 	\dens, ~dens[1]*100
// ).play

s.record;
s.stopRecording;