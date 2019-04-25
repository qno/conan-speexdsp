#include <speex/speex_jitter.h>


int main()
{
   auto* jitterBuffer = jitter_buffer_init(32);

   if (jitterBuffer)
   {
      jitter_buffer_reset(jitterBuffer);
   }

   jitter_buffer_destroy(jitterBuffer);

   return 0;
}
