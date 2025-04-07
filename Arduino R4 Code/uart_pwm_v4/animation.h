const uint32_t animation[][4] = {
	{
		0x0,
		0x0,
		0x800800,
		66
	},
	{
		0x0,
		0x8008,
		0x800800,
		66
	},
	{
		0x80,
		0x8008008,
		0x800800,
		66
	},
	{
		0x80080080,
		0x8008008,
		0x800800,
		66
	},
	{
		0x800c00c0,
		0x8008008,
		0x800800,
		66
	},
	{
		0x800c00e0,
		0xa008008,
		0x800800,
		66
	},
	{
		0x800c00e0,
		0xb009008,
		0x800800,
		66
	},
	{
		0x800c00e0,
		0xb009808,
		0x80800800,
		66
	},
	{
		0x800c00e0,
		0xb009808,
		0xc0840800,
		66
	},
	{
		0x800c00e0,
		0xb409c08,
		0xc0840840,
		66
	},
	{
		0x800c40e4,
		0xb409c08,
		0xc0840840,
		66
	},
	{
		0x840c40e4,
		0xb409c08,
		0xc0840840,
		66
	},
	{
		0x870c60e4,
		0xb409c08,
		0xc0860870,
		66
	},
	{
		0x87cc60e6,
		0xb609e08,
		0xe086087c,
		66
	},
	{
		0x87cc62e6,
		0x1b609e08,
		0xe186287c,
		66
	},
	{
		0x87cc62e6,
		0x1b619e18,
		0xe186287c,
		66
	},
	{
		0x87cc66e6,
		0x3b619e18,
		0xe386687c,
		66
	},
	{
		0xf88cccc,
		0x66c23c21,
		0xc60cc0f8,
		66
	},
	{
		0x1f119898,
		0xcd847843,
		0x8c1981f1,
		66
	},
	{
		0x3e333031,
		0x8b08f087,
		0x183303e3,
		66
	},
	{
		0x7c366063,
		0x610e10e,
		0x306607c3,
		66
	},
	{
		0xf87cc1c6,
		0x1c21c21c,
		0x61cc1f87,
		66
	},
	{
		0xf8fcc2c6,
		0x2c22c22c,
		0x62cc2f8f,
		66
	},
	{
		0xf1f9848c,
		0x48448448,
		0xc4984f1f,
		66
	},
	{
		0xe3f30918,
		0x90890891,
		0x89309e3f,
		66
	},
	{
		0xc7f61231,
		0x21131133,
		0x12612c7e,
		66
	},
	{
		0x8ffc2462,
		0x42272266,
		0x25c248fc,
		66
	},
	{
		0x1fe849c4,
		0x944e44cc,
		0x4a8491f9,
		66
	},
	{
		0x3fd09289,
		0x289c8988,
		0x940923f3,
		66
	},
	{
		0x7fb12512,
		0x51391311,
		0x291257e7,
		66
	},
	{
		0xff724a24,
		0xa2722622,
		0x5224afcf,
		66
	},
	{
		0xfee49549,
		0x54e44c44,
		0xa4495f9e,
		66
	},
	{
		0xfdd92a92,
		0xa9c99889,
		0x4892af3d,
		66
	},
	{
		0xfbb25425,
		0x43933102,
		0x90254e7b,
		66
	},
	{
		0xf764a94a,
		0x87266215,
		0x214a9cf6,
		66
	},
	{
		0xeed95395,
		0x1e4dc43a,
		0x439539ed,
		66
	},
	{
		0xdda2a62a,
		0x2c9b8864,
		0x862a63da,
		66
	},
	{
		0xbb454c54,
		0x493710c9,
		0xc54c7b4,
		66
	},
	{
		0x769a99a8,
		0x926f2192,
		0x19a99f69,
		66
	},
	{
		0xed253351,
		0x34de4324,
		0x32533ed2,
		66
	},
	{
		0xda5a66a2,
		0x69bd8648,
		0x64a66da5,
		66
	},
	{
		0xb4b4cc44,
		0xc37b0c80,
		0xc84ccb4b,
		66
	},
	{
		0x69699989,
		0x86f61911,
		0x91999696,
		66
	},
	{
		0xd2c33313,
		0x1ded3233,
		0x23333d2d,
		66
	},
	{
		0xa5966626,
		0x2bdb6466,
		0x46666a5a,
		66
	},
	{
		0x4b3ccc4c,
		0x47b7c8cc,
		0x8cccc4b4,
		66
	},
	{
		0x96699998,
		0x9f6f9199,
		0x19999969,
		66
	},
	{
		0x2cd33231,
		0x2ede2322,
		0x323322d2,
		66
	},
	{
		0x59b66562,
		0x5dbd4654,
		0x656655a5,
		66
	},
	{
		0xb37ccac4,
		0xab7a8ca8,
		0xcaccab4a,
		66
	},
	{
		0x66e99489,
		0x46f41941,
		0x94994694,
		66
	},
	{
		0xcdd32912,
		0x9de93293,
		0x29328d29,
		66
	},
	{
		0x9ba65225,
		0x2bd26526,
		0x52650a52,
		66
	},
	{
		0x374ca44a,
		0x47a4ca4c,
		0xa4ca04a4,
		66
	},
	{
		0x6e894894,
		0x8f489489,
		0x48940948,
		66
	},
	{
		0xdd029029,
		0xe902902,
		0x90280290,
		66
	},
	{
		0xba052052,
		0xd205205,
		0x20500520,
		66
	},
	{
		0x740a40a4,
		0xa40a40a,
		0x40a00a40,
		66
	},
	{
		0xe8048048,
		0x4804804,
		0x80400480,
		66
	},
	{
		0xd0090090,
		0x9009009,
		0x800900,
		66
	},
	{
		0xa0020020,
		0x2002002,
		0x200,
		66
	},
	{
		0x40040040,
		0x4004004,
		0x400,
		66
	},
	{
		0x80080080,
		0x8008008,
		0x800,
		66
	},
	{
		0x0,
		0x0,
		0x0,
		66
	}
};