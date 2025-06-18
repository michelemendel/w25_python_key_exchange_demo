# History of Cryptography

```mermaid
flowchart TB
    classDef era fill:#FFD9B3,stroke:#FF9900,stroke-width:2px,color:#663300
    classDef method fill:#FFF2CC,stroke:#FFB84D,stroke-width:1px,color:#663300

    ancient["<b>Ancient</b><br><b>Scytale (c.400 BC)</b><br>Pro: No key<br>Con: Easy break<br><br><b>Caesar (c.100 BC)</b><br>Pro: Simple<br>Con: Few keys"]
    medieval["<b>Middle Ages</b><br><b>Vigenère (1553)</b><br>Pro: Polyalpha<br>Con: Frequency analysis"]
    ww2["<b>WWII</b><br><b>Enigma (1920s-45)</b><br>Pro: Complex<br>Con: Key distrib."]
    modern["<b>Modern</b><br><b>DES (1977)</b><br>Pro: Fast<br>Con: Short key<br><br><b>AES (2001)</b><br>Pro: Strong<br>Con: Symmetric only"]
    publicKey["<b>Public Key</b><br><b>DH (1976)</b><br>Pro: Secure exchange<br>Con: MITM<br><br><b>RSA (1977)</b><br>Pro: Signatures<br>Con: Slow<br><br><b>RSA Key Transport (1990s)</b><br>Pro: Simple<br>Con: No forward secrecy"]
    current["<b>Current</b><br><b>TLS 1.3 (2018)</b><br>Pro: Forward secrecy<br>Con: Complex<br><br><b>PQC (2016–)</b><br>Pro: Quantum safe<br>Con: Experimental"]

    ancient --> medieval --> ww2 --> modern --> publicKey --> current

    class ancient,medieval,ww2,modern,publicKey,current era
```

---

## Explanation of Terms

**Frequency analysis:**
A cryptanalysis technique that studies the frequency of letters or groups of letters in a ciphertext. It exploits the fact that, in any given language, certain letters and combinations appear with predictable frequencies, making simple substitution ciphers vulnerable.

**No forward secrecy:**
A property of some encryption schemes where, if the long-term private key is compromised, all past communications encrypted with that key can also be decrypted. Forward secrecy prevents this by generating unique session keys for each communication session.

**MITM (Man-in-the-Middle):**
A type of attack where an attacker secretly intercepts and possibly alters the communication between two parties who believe they are directly communicating with each other.

**Key transport:**
A method in cryptography where one party generates a symmetric key and securely sends ("transports") it to the other party, typically using the recipient's public key for encryption. The receiving party then decrypts the key with their private key, and both parties use the shared symmetric key for further communication.

**Key agreement or key exchange**
Both parties contribute key material to jointly derive the shared secret (e.g., DH).

**Why wasn't Diffie-Hellman (DH) used in early TLS versions, despite being invented in 1976?**
Although DH was invented in 1976, it was not widely used in protocols like SSL/TLS until much later due to several reasons:

- **Patent restrictions:** DH was patented and required licensing fees, which discouraged early adoption in commercial software.
- **Performance and implementation complexity:** Early computers were less powerful, and DH computations were more resource-intensive and harder to implement securely compared to RSA key transport.
- **Market adoption:** RSA became the de facto standard for public key cryptography in the 1990s, and many systems were built around it.
- **Transition period:** Only after patents expired and the need for forward secrecy became more widely recognized did DH (and especially ephemeral DH) become the preferred method for secure key exchange in protocols like TLS 1.2 and TLS 1.3.
