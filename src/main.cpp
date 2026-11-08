#include "esp_camera.h"
#include "Arduino.h"

#define FLASH_LED_PIN 4

// Pines de la cámara AI-Thinker
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27
#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

void setup() 
{
  Serial.begin(115200);
  
  pinMode(FLASH_LED_PIN, OUTPUT);
  digitalWrite(FLASH_LED_PIN, LOW);

  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;

  // Configuración de resolución y calidad
  config.frame_size = FRAMESIZE_VGA; 
  config.jpeg_quality = 20; // Ajustado para evitar truncamientos
  config.fb_count = 1;

  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) 
  {
    Serial.printf("Error camara: 0x%x\n", err);
    return;
  }
  Serial.println("ESP32 Listo. Esperando comandos...");
}

void loop() 
{
  // ¿Hay algún byte esperando en el puerto serie?
  if (Serial.available() > 0) 
  {
    uint8_t comando = Serial.read();

    // Si el comando es 0x01, disparamos la captura
    if (comando == 0x01) 
    {
      // 1. Encender luz y estabilizar
      digitalWrite(FLASH_LED_PIN, HIGH);
      delay(300); 

      // 2. Capturar
      camera_fb_t * fb = esp_camera_fb_get();
      if (!fb) 
      {
        Serial.println("Error al capturar");
        digitalWrite(FLASH_LED_PIN, LOW);
        return;
      }

      // 3. Enviar marcadores y datos
      Serial.write(0xAA);
      Serial.write(0x55);
      Serial.write(fb->buf, fb->len);
      Serial.write(0x55);
      Serial.write(0xAA);

      // 4. Limpiar y apagar
      esp_camera_fb_return(fb);
      digitalWrite(FLASH_LED_PIN, LOW);
    }
  }
}