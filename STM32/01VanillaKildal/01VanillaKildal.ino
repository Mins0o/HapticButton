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

#define PWM_FREQ_K 25     // PWM frequency of ouput in kHz
#define BASE_FREQ 350
#define PULSE_COUNT 4
#define GRAIN_INTV 100

#define TIM2CNT (TIMER2->regs).bas->CNT

#define INACCURACY 0.57

#define INCREMENT (2 * PI)/(PWM_FREQ_K * 1000 / BASE_FREQ) / INACCURACY
#define ENV_OVF uint(PULSE_COUNT * (PWM_FREQ_K * 1000 / BASE_FREQ))



float i = 0;

bool play = true;
int played_at = 0;


void Timer4_ISR(){ // This function is called after every overflow. Update PWM threshold here.
  // PWM output is 65535 at max.

  if(play){
    // Calling sin() inside slows down quite significantly
    pwmWrite(PB7, ((sin(i)*(ENV_OVF-TIM2CNT)/ENV_OVF)+1)*36000/PWM_FREQ_K);
  }
  //pwmWrite(PB6, (sin(i)+1)*36000/PWM_FREQ_K);
  i += INCREMENT;
  if(i>2*PI){
    i=0;
  }
  if(TIM2CNT ==0  || ENV_OVF-TIM2CNT < 5){
    play = false;
    (TIMER2->regs).bas->CNT=0;
    i=0;
    pwmWrite(PB7, 36000/PWM_FREQ_K);
  }
}

void setup() {
  // Practicing register
  GPIOB->regs->CRH &= 0x44404444; // Reseting pin PB12
  GPIOB->regs->CRH |= 0x00020000; // Setting PB12 to push-pull output
  //--Still haven't figured out how to set PWM mode with registers.--//

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
  Timer2.setOverflow(ENV_OVF);
  //--------------------------//

  
  (TIMER2->regs).bas->CNT = 0;
  (TIMER4->regs).bas->CNT = 0; // Manually clearing count

  Timer4.refresh();
  Timer2.refresh();
  Timer4.resume();
  Timer2.resume();
  

  // For debugging
  //Serial1.begin(115200);
}

void loop() {
  int read_val = analogRead(PB1);
  if (abs(played_at - read_val)>GRAIN_INTV){
    played_at = read_val;
    (TIMER4->regs).bas->CNT = 0;
    (TIMER2->regs).bas->CNT = 0;
    i=0;
    play=true;
    GPIOB->regs->ODR ^= 0x00001000;
    //Serial1.println(ENV_OVF);
  }
}
