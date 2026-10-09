# HU: Unirse a una Actividad (Inscripción de Voluntarios)

## Historia de usuario

**Como** usuario voluntario (no organizador de la actividad)  
**Quiero** inscribirme a una actividad disponible desde la pantalla de detalle  
**Para** asegurar mi lugar como participante y confirmar mi asistencia  

## Criterios de aceptación

- [X] El botón "Participar" solo debe mostrarse a usuarios que no sean los dueños de la actividad.
- [X] Al hacer clic en "Participar", debe abrirse un modal de confirmación antes de registrar la plaza.
- [X] Solo se permite unirse si la actividad se encuentra en estado activa (`ACTIVE`).
- [X] Solo se permite unirse si la fecha de la actividad es futura (aún no ha transcurrido).
- [X] Solo se permite unirse si la actividad tiene cupos disponibles (`inscritos < capacidad`).
- [X] El organizador de la actividad no puede inscribirse en su propia iniciativa.
- [X] Un usuario no puede inscribirse más de una vez en la misma actividad.
- [X] El sistema debe evitar sobrecupo mediante exclusión mutua (`FOR UPDATE`) si dos usuarios intentan ganar el último cupo al mismo tiempo.
- [X] Al confirmar la asistencia con éxito, se debe guardar la participación, notificar al usuario y cambiar el botón a "Asistiré (Confirmado)".
- [X] Si los cupos están agotados, el botón debe aparecer deshabilitado con el texto "Cupos agotados".
- [X] Si la actividad está cerrada o en borrador, el botón debe aparecer deshabilitado con el texto "Convocatoria cerrada".
