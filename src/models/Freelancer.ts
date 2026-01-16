import mongoose, { Model, Document } from 'mongoose'

type AnyDoc = Document & { [key: string]: any }

const FreelancerSchema = new mongoose.Schema(
	{},
	{
		strict: false,
		strictQuery: false,
		minimize: false,
		timestamps: false,
		versionKey: false
	}
)

export const Freelancer: Model<AnyDoc> = (mongoose.models.Freelancer as Model<AnyDoc>) ||
	mongoose.model<AnyDoc>('Freelancer', FreelancerSchema, 'freelancers')
