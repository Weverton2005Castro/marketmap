const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');

const client = new Client({
	authStrategy: new LocalAuth()
});

client.on('qr', (qr) => {
	qrcode.generate(qr, { small: true });
	console.log('Escaneie o QR code acima com o WhatsApp!');
});

client.on('ready', () => {
	console.log('Bot está pronto!');
});

client.on('message', async msg => {
	if (msg.body === '123') {
		await msg.reply('oi');
	}
});

client.initialize();
