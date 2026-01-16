import fs from 'node:fs'
import path from 'node:path'
import { Readable } from 'node:stream'
import streamJsonPkg from 'stream-json'
import streamArrayPkg from 'stream-json/streamers/StreamArray.js'
import { Freelancer } from '../models/Freelancer.js'

const { parser } = streamJsonPkg as any
const { streamArray } = streamArrayPkg as any

const BATCH_SIZE = Number(process.env.SEED_BATCH_SIZE || 1000)

export async function seedIfEmpty(): Promise<void> {
	const count = await Freelancer.estimatedDocumentCount().exec()
	if (count > 0) {
		console.log(`Freelancers collection already seeded with ${count} docs`)
		return
	}

	const dataPath = process.env.FREELANCERS_PATH || path.resolve(process.cwd(), 'freelancers.json')
	if (!fs.existsSync(dataPath)) {
		console.warn(`freelancers.json not found at ${dataPath}; skipping initial seed`)
		return
	}

	console.log('Seeding freelancers from', dataPath)
	const readStream = fs.createReadStream(dataPath)
	const jsonStream = readStream.pipe(parser()).pipe(streamArray()) as Readable & AsyncIterable<{ key: number; value: any }>

	let batch: any[] = []
	let total = 0

	for await (const chunk of jsonStream) {
		batch.push(chunk.value)
		if (batch.length >= BATCH_SIZE) {
			await Freelancer.insertMany(batch, { ordered: false })
			total += batch.length
			console.log(`Seeded ${total} freelancers...`)
			batch = []
		}
	}

	if (batch.length) {
		await Freelancer.insertMany(batch, { ordered: false })
		total += batch.length
	}
	console.log(`Seeding complete. Inserted ${total} freelancers.`)
}
