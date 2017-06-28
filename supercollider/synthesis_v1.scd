//File.getcwd
//Document.dir = "Users/alexandriaguo/Documents/2016-2017/*misc/EMW/test code";

	// open file, read and put strings into array, close file.
Server.default=s=Server.local;
s.boot;

    // GRANULAR SYNTHESIS!!!
b=Buffer.alloc(s, 10*44100, 1);

//s.record;
//s.stopRecording;
s.makeWindow;

(   // square waveform INCORRECT
SynthDef(\square, {arg freq=440, amp=0.25, out=0; var wave;
	wave=Mix.fill(50,{|i| //50 = acc. of approximation of square
		var harmonicnumber=2*i+1; //odd harmonics only
		SinOsc.ar(freq*harmonicnumber) / harmonicnumber}) * amp;
	Out.ar(out,Pan2.ar(wave,0.0))}).add;)

    // visualize different possible grains (based on waveform)
({
	var freq=440;
	var grain1, grain2, grain3, grain4, grain5;
	grain1=SinOsc.ar(freq,0,XLine.kr(1.0, 0.0001, 0.05));
	grain2=Saw.ar(freq,XLine.kr(1.0, 0.0001, 0.05));
	//grain3=Synth(\square,[\freq,freq,\amp,XLine.kr(1.0, 0.0001, 0.05)]); //cannot be visualized
[grain1,grain2] //grain3
}.plot(0.1,s))

{SinOsc.ar(440,0,0.1)*EnvGen.kr(Env([1,0],[1.0]))}.scope
{EnvGen.kr(Env.adsr(0.01, 0.4, 0.2, 0.3), doneAction:2)}.plot;
Env.perc(0.01, 1, 1, -3).plot;
{XLine.kr(1.001,0.001,1,doneAction:2)}.plot(1, minval: 0, maxval: 1);
//(XLine.kr(1.001,0.001,len,doneAction:2) - 0.001)


(   // definition of grain1
SynthDef(\sinegrain, {arg pan, freq, len, amp; var grain;
	grain= SinOsc.ar(freq,0,amp) * (EnvGen.ar(Env.adsr(0.01, 0.4, 0.2, 0.3), doneAction:2));
	Out.ar(0,Pan2.ar(grain, pan))}).add;)
(   // alt definition of grain1
SynthDef(\altsinegrain, {arg pan, freq, len, amp; var grain;
	grain= SinOsc.ar(freq,0,amp) * (EnvGen.ar(Env.perc(0.01, 1, 1, -3), doneAction:2));
	Out.ar(0,Pan2.ar(grain, pan))}).add;)
(   // definition of grain2
SynthDef(\sawgrain, {arg pan, freq, len, amp; var grain;
	grain= Saw.ar(freq,amp) * (XLine.kr(1.001,0.001,len,doneAction:2) - 0.001);
	Out.ar(0,Pan2.ar(grain, pan))}).add;)
(   // definition of grain3  INCORRECT
SynthDef(\squaregrain, {arg pan, freq2, len, amp; var grain;
	grain= Synth(\square,[\freq,5,\amp,amp,\out,0]) * (XLine.kr(1.001,0.001,len,doneAction:2) - 0.001);
	Out.ar(1,Pan2.ar(grain, pan))}).add;)

    // listen to a single grain;
{Synth(\sinegrain,[\freq,rrand(100,10000),\amp, exprand(0.05,0.1), \pan, 1.0.rand2, \len, 0.1])}.plot(1, minval: 0, maxval: 1);
Synth(\altsinegrain,[\freq,rrand(100,10000),\amp, exprand(0.05,0.1), \pan, 1.0.rand2, \len, 0.1]);
Synth(\sawgrain,[\freq,rrand(100,10000),\amp, exprand(0.05,0.1), \pan, 1.0.rand2, \len, 0.1]);
Synth(\square,[\freq,440,\amp,XLine.kr(1.0, 0.0001, 0.05)]); // NOT FUNCTIONAL

(
var biota, toyinput;
biota = asFloat(CSVFileReader.read("/Users/alexandriaguo/Documents/2016-2017/*misc/EMW/test code/scdInput.csv", true).postcs);
biota = biota.flop;
toyinput = [0.0174,0.0190,0.0290,0.0088,0.0083];
//the average is ~0.0165, reciprocal ~60
toyinput.size.postln;
//{Mix.new(SinOsc.ar(biota[2], 0, 0.1))}.play; //Additive Synthesis
)
[223, 332,14].scramble.postln;
[223, 332,14].size;

({    // SECTOR 1 data, 7 colonies (NOTE: SET EQUAL TO A VARIABLE!)
	var col=[30, 30, 30, 30, 152.567, 201.444, 197.423];
	var dens=0.0174;
	10.do{ arg i;
		var diam = col.scramble;
		col.size.do{ arg j;
		var timeprop = (i/(col.size - 1))**3;
			diam[i].postln;
			Synth(\altsinegrain,[
				\freq, diam[j],
				\amp, exprand(0.05,0.1),
				\pan, 1.0.rand2,
				\len,(dens*20)/col.size]);
			timeprop*((1-dens)/(2*col.size)).wait
		}
};
}.fork;)

({    // SECTOR 2 data, 9 colonies
	var col=[1434.136, 116.132, 1123.645, 116.132, 199.6547, 1191.98, 116.132, 4000, 3138.221];
	var dens=0.0190;
	25.do{ arg i;
		var diam = col.scramble;
		col.size.do{ arg j;
		var timeprop = (i/(col.size - 1))**3;
			diam[i].postln;
			Synth(\sinegrain,[
				\freq, diam[j],
				\amp, exprand(0.05,0.1),
				\pan, 1.0.rand2,
				\len,(dens*20)/col.size]);
			timeprop*((1-dens)/(2*col.size)).wait
		}
};
}.fork;)

({    // SECTOR 3 data, 11 colonies
	var col=[169.7876, 1227.020, 30,  490.284, 268.4555, 557.1865, 30, 30, 30, 1046.615, 30];
	var dens=0.0290;
	25.do{ arg i;
		var diam = col.scramble;
		col.size.do{ arg j;
		var timeprop = (i/(col.size - 1))**3;
			diam[i].postln;
			Synth(\sinegrain,[
				\freq, diam[j],
				\amp, exprand(0.05,0.1),
				\pan, 1.0.rand2,
				\len,(dens*20)/col.size]);
			timeprop*((1-dens)/(2*col.size)).wait
		}
};
}.fork;)

({    // SECTOR 4 data, 11 colonies
	var col=[30, 30, 1880.615, 116.132, 1240.983, 30, 30, 1165.589, 30, 116.132, 116.132];
	var dens=0.0088;
	25.do{ arg i;
		var diam = col.scramble;
		col.size.do{ arg j;
		var timeprop = (i/(col.size - 1))**3;
			diam[i].postln;
			Synth(\sinegrain,[
				\freq, diam[j],
				\amp, exprand(0.05,0.1),
				\pan, 1.0.rand2,
				\len,(dens*20)/col.size]);
			timeprop*((1-dens)/(2*col.size)).wait
		}
};
}.fork;)

({    // SECTOR 5 data, 5 colonies
	var col=[1633.5635, 30, 116.132, 30, 116.132];
	var dens=0.0083;
	25.do{ arg i;
		var diam = col.scramble;
		col.size.do{ arg j;
		var timeprop = (i/(col.size - 1))**3;
			diam[i].postln;
			Synth(\sinegrain,[
				\freq, diam[j],
				\amp, exprand(0.05,0.1),
				\pan, 1.0.rand2,
				\len,(dens*20)/col.size]);
			timeprop*((1-dens)/(2*col.size)).wait
		}
};
}.fork;)

(
SynthDef(\demo, { ||
	var env = XLine(1.001, 0.001, 0.1),
	sig = SinOsc;
};
))
/*({   // TESTING!
//SynthDef(\granularsine, {arg col=[223, 332, 442], dens=0.02; var diam;
    var col=Array.rand(200, 100, 1000); var dens=0.02;
	var diam = col.scramble;
	col.size.do{arg i;
		var timeprop = (i/(col.size - 1))**3;

		Synth(\sinegrain,[
			\freq, col[i],
			\amp, exprand(0.05,0.1),
			\pan, 1.0.rand2]);
		rrand((timeprop*0.1).max(dens),timeprop*0.3).wait
};
}.fork;)
//}
//}.fork;))*/