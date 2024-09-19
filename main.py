from flask import Flask, request, render_template_string
import serial
import serial.tools.list_ports
import os

# Flask 앱 초기화
app = Flask(__name__)

# 업로드된 파일을 저장할 폴더
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 사용 가능한 UART 포트 목록을 가져오는 함수
def get_available_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

# 비트스트림 파일을 UART로 전송하는 함수
def send_bitstream_via_uart(filepath, uart_port, baudrate):
    try:
        with serial.Serial(uart_port, baudrate, timeout=1) as uart:
            with open(filepath, 'rb') as bitstream_file:
                while (chunk := bitstream_file.read(1024)):  # 1KB씩 전송
                    uart.write(chunk)
            return True
    except serial.SerialException as e:
        print(f"UART 통신 오류: {e}")
        return False

# 비트스트림 파일 업로드 및 전송 경로
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    available_ports = get_available_ports()
    
    if request.method == 'POST':
        # 선택된 UART 포트와 Baudrate 값 가져오기
        uart_port = request.form.get('port')
        baudrate = int(request.form.get('baudrate'))
        
        if 'file' not in request.files:
            message = '파일을 선택하지 않았습니다.'
            return render_template_string(form_template, available_ports=available_ports, message=message, message_type='danger')
        
        file = request.files['file']
        if file.filename == '':
            message = '선택된 파일이 없습니다.'
            return render_template_string(form_template, available_ports=available_ports, message=message, message_type='danger')
        
        if file and file.filename.endswith('.bit'):  # 비트스트림 파일 체크
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            success = send_bitstream_via_uart(filepath, uart_port, baudrate)
            if success:
                message = f'파일 <strong>{file.filename}</strong>이(가) <strong>{uart_port}</strong> 포트와 <strong>{baudrate}</strong> Baudrate로 FPGA에 전송되었습니다!'
                return render_template_string(form_template, available_ports=available_ports, message=message, message_type='success')
            else:
                message = 'UART를 통해 파일 전송에 실패했습니다.'
                return render_template_string(form_template, available_ports=available_ports, message=message, message_type='danger')
        else:
            message = '유효한 .bit 파일을 업로드해주세요!'
            return render_template_string(form_template, available_ports=available_ports, message=message, message_type='danger')
    
    # 초기 페이지 로드 시 메시지 없음
    return render_template_string(form_template, available_ports=available_ports, message=None, message_type=None)

# HTML 폼 템플릿 (Bootstrap 사용)
form_template = '''
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>비트스트림 파일 업로드</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
      body {
        background-color: #f8f9fa;
      }
      .container {
        max-width: 600px;
        margin-top: 50px;
        padding: 20px;
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h2 class="mb-4 text-center">FPGA 비트스트림 파일 업로드</h2>
      
      {% if message %}
      <div class="alert alert-{{ message_type }} alert-dismissible fade show" role="alert">
        {{ message | safe }}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="닫기"></button>
      </div>
      {% endif %}
      
      <form method="post" enctype="multipart/form-data">
        <div class="mb-3">
          <label for="port" class="form-label">UART 포트 선택</label>
          <select class="form-select" id="port" name="port" required>
            <option value="" disabled selected>포트를 선택하세요</option>
            {% for port in available_ports %}
              <option value="{{ port }}">{{ port }}</option>
            {% endfor %}
          </select>
        </div>
        
        <div class="mb-3">
          <label for="baudrate" class="form-label">Baudrate 선택</label>
          <select class="form-select" id="baudrate" name="baudrate" required>
            <option value="" disabled selected>Baudrate를 선택하세요</option>
            <option value="9600">9600</option>
            <option value="19200">19200</option>
            <option value="38400">38400</option>
            <option value="57600">57600</option>
            <option value="115200">115200</option>
          </select>
        </div>
        
        <div class="mb-3">
          <label for="file" class="form-label">비트스트림 파일 업로드 (.bit)</label>
          <input class="form-control" type="file" id="file" name="file" accept=".bit" required>
        </div>
        
        <div class="d-grid">
          <button type="submit" class="btn btn-primary">업로드 및 전송</button>
        </div>
      </form>
    </div>

    <!-- Bootstrap JS (Optional: for dismissible alerts) -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
  </body>
</html>
'''

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')  # 네트워크에서 접근 가능하도록 서버 실행
