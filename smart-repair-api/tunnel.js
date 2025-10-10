// tunnel.js
const { spawn } = require('child_process');
const https = require('https');
const fs = require('fs');

console.log('🚀 Starting LocalTunnel with PM2 (Auto-Restart)...');

// تابع دریافت و نمایش پسورد
function getAndShowPassword() {
    return new Promise((resolve) => {
        console.log('🔑 Getting tunnel password...');
        
        const req = https.get('https://loca.lt/mytunnelpassword', (res) => {
            let data = '';
            res.on('data', (chunk) => data += chunk);
            res.on('end', () => {
                const password = data.trim();
                if (password) {
                    console.log('\n' + '='.repeat(60));
                    console.log('🔑 TUNNEL PASSWORD:', password);
                    console.log('🌐 TUNNEL URL: https://hadisadoghiyazdi.loca.lt');
                    console.log('='.repeat(60) + '\n');
                    
                    // ذخیره در فایل برای دسترسی آسان
                    fs.writeFileSync('current-password.txt', password);
                    console.log('💾 Password saved to current-password.txt');
                }
                resolve(password);
            });
        });

        req.on('error', () => {
            console.log('⚠️  Could not get password automatically');
            console.log('🔗 Please visit: https://loca.lt/mytunnelpassword');
            resolve(null);
        });

        req.setTimeout(10000, () => {
            req.destroy();
            console.log('⏰ Timeout getting password');
            resolve(null);
        });
    });
}

// تابع شروع تونل
function startTunnel() {
    console.log('🌐 Starting localtunnel process...');
    
    const tunnel = spawn('npx', ['localtunnel', '--port', '5000', '--subdomain', 'hadisadoghiyazdi'], {
        stdio: 'pipe',
        shell: true
    });

    tunnel.stdout.on('data', (data) => {
        const output = data.toString().trim();
        console.log(`[TUNNEL] ${output}`);
        
        if (output.includes('your url is:')) {
            console.log('✅ Tunnel is ready and running...');
        }
    });

    tunnel.stderr.on('data', (data) => {
        console.error(`[TUNNEL-ERROR] ${data.toString().trim()}`);
    });

    tunnel.on('close', (code) => {
        console.log(`❌ Tunnel process exited with code ${code}`);
        console.log('🔄 PM2 will automatically restart this process...');
        
        // PM2 به طور خودکار ریستارت می‌کند
        process.exit(code || 1);
    });

    tunnel.on('error', (err) => {
        console.error('❌ Tunnel process error:', err);
    });

    return tunnel;
}

// اجرای اصلی
async function main() {
    await getAndShowPassword();
    startTunnel();
}

main();

// لاگ دوره‌ای برای نشان دادن فعالیت
setInterval(() => {
    console.log('💚 Tunnel monitor: still running...', new Date().toLocaleTimeString());
}, 60000); // هر 1 دقیقه