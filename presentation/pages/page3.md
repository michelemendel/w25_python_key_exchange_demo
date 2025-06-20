### Diffie-Hellman Mathematics

<div class="grid grid-cols-2 gap-8 items-center">

<div style="text-align: center;">

$$s = g^{ab}\mod p$$

<div style="font-size: 0.5em;">
The security of Diffie-Hellman relies on the difficulty<br/>of the discrete logarithm problem
</div>

</div>

<div style="font-size: 0.7em; margin-top: 20px;">

<div class="list-header">p (prime modulus)</div>

- A large prime number agreed upon by both parties
- p should be a safe prime (i.e. (p-1)/2 is also prime) to prevent certain attacks
- Common sizes: At least 2048 bits for modern security

<div class="list-header">g (generator)</div>

- A number less than p, also agreed upon by both parties
- g should be a primitive root modulo p, meaning its powers generate all numbers from 1 to p-1
- Common values: 2 or 5 are often used, but must be chosen carefully with p

<div class="list-header">a, b (private secrets)</div>

- Randomly chosen integers, kept secret by both sides
- Common sizes: Should be at least as large as the bit length of p (e.g., 2048 bits)

</div>

</div>

<style>
ul li {
  font-size: 0.6em !important;
}

.list-header {
  font-size: 0.9em !important;
  font-weight: bold !important;
  margin-top: 10px !important;
  margin-bottom: 5px !important;
}
</style>
