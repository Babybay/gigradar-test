declare module 'stream-json' {
	import { Transform } from 'stream'
	const streamJson: {
		parser(options?: any): Transform
	}
	export default streamJson
}

declare module 'stream-json/streamers/StreamArray.js' {
	import { Transform } from 'stream'
	const streamArrayModule: {
		streamArray(): Transform
	}
	export default streamArrayModule
}

