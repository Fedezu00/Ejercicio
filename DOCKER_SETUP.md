# DOCKER_SETUP.md

## 1. ¿Qué pasa si corremos la imagen de Docker sin asignar ninguna flag a `docker run`? ¿Podemos usar la misma terminal para correr otros comandos?



---

## 2. El proyecto usa el puerto 5000. Intentar hacer `docker run` con y sin el parámetro correspondiente. ¿Qué ocurre en cada caso?


- **Con el parámetro `-p 5000:5000`:**

---

## 3. Ejecutar `docker stop <container>`. ¿Qué pasa si al hacer `docker run` no le asigno un nombre al contenedor? ¿Qué debo poner en `<container>` para poder hacer `docker stop <container>`?

Si no asignas un nombre al contenedor con `--name`, Docker le asigna un nombre aleatorio. Para detenerlo, necesitas el **ID** o el **nombre** del contenedor. Puedes obtenerlo con:



---

## 4. Si corro el contenedor en segundo plano, no veo información de la dirección IP que necesito para usar mi proyecto. Documentar qué se debe poner en el navegador
