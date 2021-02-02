// Two pins required:
// - One for sensor input
// - One for signal output
//
// PWM duty cycle should be adjustable in the corresponding timer interrupt
// Timer overflow should be set to be greater so the frequency is higher than 20k,
//  but still small for accurate output
// 
// For enveloped grain output, another timer should be setup.
// Counting of this timer will be used in order to adjust the envelope length.

//--------User Variables---------//
#define PWM_FREQ_K 25     // PWM frequency of ouput in kHz
//#define BASE_FREQ 300     // Base frequency of the sinewave vibration
//#define PULSE_COUNT 5     // Half cycles of base sinewave that fits in an envelope
//#define GRAIN_INTV 100    // Force interval between grains.
//-------------------------------//

#define TIM2CNT (TIMER2->regs).bas->CNT // Making it shorter
#define A_IN_LOW ((GPIOA->regs->IDR) & 0x000001fc) >> 2

#define INACCURACY 0.57//25k// Inaccuracy of frequency cuased by heavy function call in interrupt

//#define INCREMENT (2 * PI)/(PWM_FREQ_K * 1000 / BASE_FREQ) / INACCURACY // Pulled out of interrupt for better performance
//#define ENV_OVF uint(PULSE_COUNT * (PWM_FREQ_K * 1000 / BASE_FREQ))     // Determines length of  single envelope


float i = 0;    // Parameter for sin().

bool play = true;     // Signal play flag
int played_at = 0;    // Keeps record of the force level 

float amp_scaler = 0.5;
uint base_freq = 300;
uint pulse_count = 5;
uint grain_intv = 100;

float increment = (2 * PI)/(PWM_FREQ_K * 1000 / base_freq) / INACCURACY;
uint env_ovf = pulse_count * (PWM_FREQ_K * 1000 / base_freq);

void Timer4_ISR(){ // This function is called after every overflow. Update PWM threshold here.
  // PWM output is 65535 at max.

  if(play){
    // Calling sin() inside slows down quite significantly
    pwmWrite(PB7, ((sin(i)*(env_ovf-TIM2CNT)/env_ovf) * amp_scaler + 1)*36000/PWM_FREQ_K);
  }
  
  //---Debugging purpose line---//
  //pwmWrite(PB6, (sin(i)+1)*36000/PWM_FREQ_K);
  //----------------------------//
  
  i += increment;
  if(i>2*PI){
    i=0;
  }
  if(TIM2CNT ==0  || env_ovf-TIM2CNT < 5){
    play = false;
    TIM2CNT=0;
    i=0;
    pwmWrite(PB7, 36000/PWM_FREQ_K);
  }
}

void setup() {
  GPIOB->regs->CRH &= 0x44404444; // Reseting pin PB12, Grain-passed indicator
  GPIOB->regs->CRH |= 0x00020000; // Setting PB12 to push-pull output

  GPIOA->regs->CRH &= 0xfffffff8;
  GPIOA->regs->CRH |= 0x00000008;
  GPIOA->regs->CRL &= 0x88888888;
  GPIOA->regs->CRL |= 0x88888888;
  GPIOA->regs->ODR &= 0x00000000;
  GPIOA->regs->ODR |= 0x000001fc; // Pull up input

  // Preset fuction from library
  pinMode(PB1, INPUT_ANALOG);
  pinMode(PB7, PWM);
  // debugging pin for frequency probing
  pinMode(PB6, PWM);

  //-------Timers------//
  //----Setting up timer 4----//
  Timer4.pause();
  
  Timer4.setPrescaleFactor(1); // Fastest counting
  Timer4.setOverflow(72000/PWM_FREQ_K); // Setting PWM frequency in kHz
  Timer4.attachInterrupt(4, Timer4_ISR); // Timer4_ISR() will be called whenever Timer 4 overflows
  //--------------------------//

  //----Setting up timer 2----//
  Timer2.pause();

  Timer2.setPrescaleFactor(uint32(36000/PWM_FREQ_K));
  Timer2.setOverflow(env_ovf);
  //--------------------------//

  
  (TIMER2->regs).bas->CNT = 0;
  (TIMER4->regs).bas->CNT = 0; // Manually clearing count

  Timer4.refresh();
  Timer2.refresh();
  Timer4.resume();
  Timer2.resume();
  

  // For debugging
  Serial1.begin(115200);
}

void loop() {
  int read_val = analogRead(PB1);
  if(A_IN_LOW & 0b1){
    amp_scaler = 0.3;
  }else{
    amp_scaler = 0.625;
  }
  
  if(A_IN_LOW & 0b10){
    grain_intv = 300;
  }else{
    grain_intv = 150;
  }
  
  if(A_IN_LOW & 0b100){
    base_freq = 300;
  }else{
    base_freq = 180;
    amp_scaler *= 1.6;
  }
  
  if(A_IN_LOW & 0b1000){
    pulse_count = 5;
  }else{
    pulse_count = 3;
  }

  increment = 0.006283185/(PWM_FREQ_K / float(base_freq)) / INACCURACY;
  env_ovf = pulse_count * (PWM_FREQ_K * 1000 / base_freq);

  Timer2.pause();
  Timer2.setOverflow(env_ovf);
  Timer2.resume();
  
  if (abs(played_at - read_val)>grain_intv){ // If increased or decreased far enough from last played

    
    
    played_at = read_val;           // 1. Keep record
    (TIMER4->regs).bas->CNT = 0;    // 2. Reset counters
    (TIMER2->regs).bas->CNT = 0;
    i=0;
    play=true;                      // 3. Set play flag
    GPIOB->regs->ODR ^= 0x00001000; // 4. Grain-passed indicator
    Serial1.print(env_ovf);
  }
}
