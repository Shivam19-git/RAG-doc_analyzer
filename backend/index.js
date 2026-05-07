const http = require('http')

const express = require('express')
const cors = require('cors')
const multer = require('multer') //handling file uploads

const app = express()
app.use(express.json())
const PORT = 3000

app.use(cors({
  origin: 'http://localhost:5173',
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type']
}))

// setup multer to store uploaded files into an upload directory
const upload = multer({dest : './uploads'})


app.get('/',(req,res,next)=>{
    res.send("Hello World")
})

app.post('/api/chat',(req,res)=>{
    const userMessage = req.body.message
    console.log(`user message ${userMessage}`)

    res.json({
        message: `Server says : ${userMessage}`
    })
})

app.listen(PORT,()=>{
    console.log(`Server running on http://localhost:${PORT}`)
})