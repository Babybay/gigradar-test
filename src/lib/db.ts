import mongoose from 'mongoose'
import dotenv from 'dotenv'

dotenv.config()

const DEFAULT_URI = 'mongodb://mongo:27017/de_gig'

export async function connectToDatabase(): Promise<void> {
	const uri = process.env.MONGO_URL || DEFAULT_URI
	mongoose.set('strictQuery', false)
	let attempts = 0
	while (true) {
		try {
			await mongoose.connect(uri, {
				serverSelectionTimeoutMS: 5000
			})
			console.log('Connected to MongoDB')
			break
		} catch (err: any) {
			attempts += 1
			const delayMs = Math.min(1000 * Math.pow(2, Math.min(attempts, 5)), 15000)
			console.warn(`MongoDB connection failed (attempt ${attempts}), retrying in ${Math.round(delayMs/1000)}s...`, err?.message)
			await new Promise((r) => setTimeout(r, delayMs))
		}
	}
}
