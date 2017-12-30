# MUII - Sistemas Cognitivos - Proyecto Final

Para crear el fichero **drugs.json**, ejecuta el siguiente comando:

```sh
$ python parse-drugs.py
```

## 1. Medicamentos
El formato de cada medicamento, que ha tomado cierto paciente, es el siguiente:

> <nombre del medicamento> <cantidad del medicamento> <dosis del paciente>

Cada segmento contiene:
  - **name**: Tipo *String*. Texto que puede contener caracteres, numeros y espacios.
  - **unit**: Tipo *Array*. Opcional. Cantidades con su unidad de medida.
  - **dose**: Tipo *String*. Opcional. Las dosis que el paciente tomo durante o cada cierto tiempo.

Un ejemplo basico:

> tranxilium 5-- 1u/d

### 1.1 Cantidad del medicamento

Cada cantidad esta acompañada de su unidad de medida (en caso de no conocerlo, esta acompañada de la expresión **--**):

> 500mg
> 500%
> 500--

También pueden darse fracciones:

> 500--/10--
> 500--/mcg

### 1.2 Dosis del paciente

Un ejemplo es el siguiente:

> 1u/2d
> 1u/s

Con esta expresión se entiende que el paciente tomó dicho medicamento cada 2 dias o cada semana.
