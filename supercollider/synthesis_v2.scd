Server.default=s=Server.local;
s.boot;
Server.local.options.numOutputBusChannels = 8;
Server.local.options.numInputBusChannels = 8;

( // DATA
// col0 -> a; col1 -> b; col2 -> c; col3 -> d; col4 -> e;
// alt: try Pxrand, Pwalk
// add remaining buffers
~dens = [0.0174, 0.0190, 0.0290, 0.0088, 0.0083];
~col0 = Pshuf([30, 30, 30, 30, 152.567, 201.444, 197.4234],1);
a=Buffer.read(s, Platform.resourceDir +/+ "sounds/funk.aiff");
~col1 = Pshuf([1434.136, 116.132, 1123.645, 116.132, 199.6547, 1191.98, 116.132, 4000, 3138.221], 1);
~col2 = Pshuf([169.788, 1227.0205, 30, 490.284, 268.456, 557.1865, 30, 30, 30, 1046.615, 30], 1);
~col3 = Pshuf([30, 30, 1880.615, 116.132, 1240.983, 30, 30, 1165.589, 30, 116.132, 116.132], 1);
~col4 = Pshuf([1633.564, 30, 116.132, 30, 116.132], 1);
)


s.sendMsg(\b_allocRead, 10, Platform.resourceDir +/+ "sounds/a11wlk01.wav");

( // MAY CHANGE ENVELOPE
SynthDef(\grain, {
	arg gdur=0.02, buf=0, rate=1, spos=0, pan=0, amp=0.5, out=0, dens;
	var trig, env, sig;
	trig = Impulse.ar(dens*1000);
	//trig = Dust.ar(dens);
	//env = EnvGen.kr(Env.sine(gdur), doneAction:2);
	//env = EnvGen.kr(Env.perc(0.01,gdur), doneAction:2);
	env = EnvGen.kr(Env([0.2,1.0,0.0],[0.1,3.0], levelScale:gdur, doneAction:2));
	sig = PlayBuf.ar(1, buf, BufRateScale.kr(buf)*rate, trig, startPos:spos, loop:1);
	sig = sig * env;
	sig = Pan2.ar(sig,pan,amp);
	Out.ar(out, sig);
}).add;
)

(
SynthDef(\testing, {arg gate=1, amp=1, rate=10, sndbuf;
	var trig, dur, modfreq, index, pan, env;
	trig = Impulse.ar(rate);
	dur = rate.reciprocal;
	modfreq = LFTri.kr(0.1).exprange(200, 840);
	index = LFCub.kr(0.2).range(4, 10);
	pan = WhiteNoise.ar.range(-0.1, 0.1);
	env = EnvGen.kr(
		Env([0, 1, 0], [1, 1], \sin, 1),
		gate, levelScale: amp, doneAction: 2);
	rate = Pseg(Pseq([0, a.numFrames],inf), Pseq([a.duration,0],inf), \lin);
	Out.ar(0,
		GrainBuf.ar(2, trig, dur, sndbuf, modfreq, rate, pan: pan) * env)
}).add;
)

a.play;
c = Synth(\testing, [\sndbuf, a, \rate, 0.190, \amp, 0.5]);
b = Synth(\testing, [\rate, 42, \amp, 0.2]);

(
x = Pbind(
	\instrument, \grain,
	\dur, 0.1,
	\gdur, 0.02,
	\buf, a.bufnum,
	\rate, 1,
	\spos, Pseg(Pseq([0, a.numFrames],inf), Pseq([a.duration,0],inf), \lin),
	\pan, 1.0.rand2,
	\amp, 0.5,
	\out, 0,
	\dens, 0.090
).play;
)

x.stop;


(
SynthDef.new(\sinegrain, {
	arg freq=440, amp=0.3, pan=0;
	var sig, env;
	sig = SinOsc.ar(freq, 0, amp);
	//sig = LFTri.ar(freq)!2;
	env = EnvGen.kr(Env([0.2,1.0,0.0],[0.1,3.0], doneAction:2));
	//env = EnvGen.kr(Env.perc(0.01,2), doneAction:2);
	//env = EnvGen.kr(Env.adsr, doneAction:2);
	sig = sig * env;
	Out.ar(0, Pan2.ar(sig, pan));
}).add;
)

(
SynthDef.new(\bufgrain, {
	arg bufnum=0, pan = 0.0, startPos=0.0, amp=0.1, dur=0.04;
	var sig, env;
	sig = PlayBuf.ar(1, bufnum, BufRateScale.kr(bufnum), 1, BufFrames.ir(bufnum)*startPos, 0);
	env = EnvGen.kr(Env.perc(0.01, dur), doneAction:2) - 0.001;
	sig = sig * env;
	Out.ar(0, Pan2.ar(sig, pan));
}).add;
)

//TESTING MUSIC PLAYBACK
({    // SECTOR 1 data, 9 colonies (NOTE: SET ROUTINE EQUAL TO A VARIABLE!)
	var col=[1434.136, 116.132, 1123.645, 116.132, 199.6547, 1191.98, 116.132, 4000, 3138.221];
	var dens=0.0174;
	10.do{ arg i;
		var diam = col.scramble;
		col.size.do{ arg j;
		var timeprop = (i/(col.size - 1))**3;
			Synth(\bufgrain,[
				\bufnum, b.bufnum,
				\pan, 1.0.rand2,
				\startPos, rrand(0.0, 1.0), //adjust for different samples
				\amp, exprand(0.005, 0.1),
				\dur, 0.4
			]);
			timeprop*((1-dens)/(2*col.size)).wait
		}
};
}.fork;)

({    // SECTOR 1 data, 0 colonies
	var col=[1434.136, 116.132, 1123.645, 116.132, 199.6547, 1191.98, 116.132, 4000, 3138.221];
	var dens=0.0174;
	10.do{ arg i;
		var diam = col.scramble;
		col.size.do{ arg j;
		var timeprop = (i/(col.size - 1))**3;
			Synth(\sinegrain,[
				\freq, diam[j],
				\amp, exprand(0.05,0.1),
				\pan, 1.0.rand2]);
			timeprop*((1-dens)/(2*col.size)).wait
		}
};
}.fork;)