# MUII - Sistemas Cognitivos - Proyecto Final

Para crear el fichero **drugs.json**, ejecuta el siguiente comando:

```sh
$ python parse-drugs.py
```

Para crear el fichero **kidney-fail.json**, ejecuta el siguiente comando:

```sh
$ python parse-kidney-fail.py
```

## 1. Medicamentos

El formato de cada medicamento, que ha tomado cierto paciente, es el siguiente:

> <nombre del medicamento> <cantidad del medicamento> <dosis del paciente>

Cada segmento contiene:
  - **name**: Tipo *String*. Texto que puede contener caracteres, numeros y espacios.
  - **unit**: Tipo *Array*. Opcional. Cantidades con su unidad de medida.
  - **dose**: Tipo *String*. Opcional. Las dosis que el paciente tomo durante o cada cierto tiempo.

Un ejemplo basico: **tranxilium 5-- 1u/d**

### 1.1 Cantidad del medicamento

Cada cantidad esta acompañada de su unidad de medida (en caso de no conocerlo, esta acompañada de la expresión **--**):

* 500mg
* 500%
* 500--

También pueden darse fracciones:

* 500--/10--
* 500--/mcg

### 1.2 Dosis del paciente

Un ejemplo es el siguiente:

* 1u/2d
* 1u/s

Con esta expresión se entiende que el paciente tomó dicho medicamento cada 2 dias o cada semana.

## 2. Formatos del dataset kidney-fail

* **blood_sugar_level**: Tipo: float. Unidad: mg/dl. Niveles de azúcar en sangre.
* **bmi**: Tipo: float. Unidad: kg/m2. Indice de masa corporal.
* **bun**: Tipo: float. Unidad: mg/dl. Nitrógeno ureico en sangre.
* **height**: Tipo: float. Unidad: cm. Altura.
* **kidney_failure**: Tipo: boolean. Si el paciente ha sufrido un fallo renal.
* **weight**: Tipo: float. Unidad: kg. Peso.
* **basophils**: Tipo: float. Unidad: %. Basófilos.
* **eosinophils**: Tipo: float. Unidad: %. Eosinófilos.
* **granulocytes**: Tipo: float. Unidad: %. Granulocitos.
* **monocytes**: Tipo: float. Unidad: %. Monocitos.
* **platelet_count**: Tipo: float. Unidad: 10^9/L. Conteo de plaquetas.
* **trgld**: ??? Unknown variable. No information provided by the hospital.
* **tflr**: ??? Unknown variable. No information provided by the hospital.
* **mean_platelet_volume**: Mean value of platelet volume.
* **leukocytes**: Leukocytes value.

## 3. Referencias

* [Blood sugar chart](https://www.diabetesselfmanagement.com/managing-diabetes/blood-glucose-management/blood-sugar-chart/)
* [Valores normales de azucar en sangre](https://www.news-medical.net/health/Blood-Sugar-Normal-Values-(Spanish).aspx)
