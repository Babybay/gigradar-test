import express, { Request, Response } from 'express'
import morgan from 'morgan'
import cors from 'cors'
import dotenv from 'dotenv'
import { connectToDatabase } from './lib/db.js'
import { seedIfEmpty } from './lib/seed.js'
import { Freelancer } from './models/Freelancer.js'

dotenv.config()

const app = express()
const PORT = process.env.PORT ? Number(process.env.PORT) : 3002
const MAX_LIMIT = 10 // Guard: maximum rows per request, enforced

app.use(cors())
app.use(express.json({ limit: '2mb' }))
app.use(morgan(process.env.NODE_ENV === 'production' ? 'combined' : 'dev'))

app.get('/healthz', (_req: Request, res: Response) => {
	res.json({ ok: true, uptimeSec: Math.round(process.uptime()) })
})

app.get('/freelancers', async (req: Request, res: Response) => {
	try {
		const limitParam = parseInt(String(req.query.limit ?? String(MAX_LIMIT)), 10)
		const pageParam = parseInt(String(req.query.page ?? '1'), 10)
		// Guard: cap limit at MAX_LIMIT (10) - if user requests more than 10, it becomes 10
		const limit = Number.isFinite(limitParam) && limitParam > 0 ? Math.min(limitParam, MAX_LIMIT) : MAX_LIMIT
		const page = Number.isFinite(pageParam) && pageParam > 0 ? pageParam : 1

		const skip = (page - 1) * limit
		const [items, total] = await Promise.all([
			Freelancer.find({}).skip(skip).limit(limit).lean().exec(),
			Freelancer.estimatedDocumentCount().exec()
		])
		const totalPages = Math.max(1, Math.ceil(total / limit))
		res.json({
			page,
			limit,
			total,
			totalPages,
			hasNextPage: page < totalPages,
			hasPrevPage: page > 1,
			items
		})
	} catch (err) {
		console.error('GET /freelancers error:', err)
		res.status(500).json({ error: 'Internal server error' })
	}
})

async function main() {
	await connectToDatabase()
	await seedIfEmpty()
	app.listen(PORT, () => {
		console.log(`API listening on :${PORT}`)
	})
}

main().catch((err) => {
	console.error('Fatal startup error:', err)
	process.exit(1)
})
