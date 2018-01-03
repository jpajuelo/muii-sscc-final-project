# MUII - Sistemas Cognitivos - Proyecto Final

Ejecutando el siguiente comando, sobreescribe los ficheros de salida que se encuentran en el directorio [outfiles](https://github.com/jpajuelo/muii-sscc-final-project/tree/develop/outfiles).

```sh
$ python clean.py
```

## 1. Información del paciente

* **basophil**: Tipo: float. Unidad: %. Basófilos.
* **blood_mass_index**: Tipo: float. Unidad: kg/m2. Indice de masa corporal.
* **blood_sugar**: Tipo: float. Unidad: mg/dl. Niveles de azúcar en sangre.
* **blood_urea_nitrogen**: Tipo: float. Unidad: mg/dl. Nitrógeno ureico en sangre.
* **eosinophil**: Tipo: float. Unidad: %. Eosinófilos.
* **height**: Tipo: float. Unidad: cm. Altura.
* **kidney_failure**: Tipo: boolean. Si el paciente ha sufrido un fallo renal.
* **mean_platelet_volume**: Tipo: float. Unidad: fL. Volumen plaquetario medio.
* **monocyte**: Tipo: float. Unidad: %. Monocitos.
* **neutrophil**: Tipo: float. Unidad: %. Neutrofilos o granulocitos.
* **platelet**: Tipo: float. Unidad: 10^9/L. Conteo de plaquetas.
* **tflr**: ??? Unknown variable. No information provided by the hospital.
* **triglyceride**: Tipo: float. Unidad: mg/dl. Triglicéridos.
* **weight**: Tipo: float. Unidad: kg. Peso.
* **white_blood_cell**: Tipo: float. Unidad: 10^9/L. Conteo de glóbulos blancos o leucocitos.

## 2. Medicamentos del paciente

El formato de cada medicamento, que ha tomado cierto paciente, es el siguiente:

```
<nombre del medicamento> <cantidad del medicamento> <dosis del paciente>
```

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

## 3. Referencias

* [BMI table](http://www.calculator.net/bmi-calculator.html)
* [Blood sugar chart](https://www.diabetesselfmanagement.com/managing-diabetes/blood-glucose-management/blood-sugar-chart/)
* [BUN test](https://www.healthline.com/health/bun)
* [Valores normales de azucar en sangre](https://www.news-medical.net/health/Blood-Sugar-Normal-Values-(Spanish).aspx)
* [Blood sugar test](https://medlineplus.gov/ency/article/003482.htm)
* [Leucocitos](https://tuchequeo.com/leucocitos-altos-en-sangre-leucositosis-causas/)
* [WBC count](https://www.healthline.com/health/wbc-count)
* [WBC count and differential](https://www.rnceus.com/cbc/cbcwbc.html)
* [Differential blood count](https://emedicine.medscape.com/article/2085133-overview)
* [Platelet count](https://medlineplus.gov/ency/article/003647.htm)
* [Kidney failure](https://www.healthline.com/health/kidney-failure#diagnosis)
* [Grunulocytosis](https://www.healthline.com/health/granulocytosis)
* [Understading your blood results](https://www.cllsupport.org.uk/cll-sll/start-here/understanding-your-blood-results)
* [Analisis de sangre](http://valencia.nueva-acropolis.es/valencia-articulos/207-pagina-de-salud/24662-claves-para-descifrar-un-analisis-de-sangre)
* [Volumen plaquetario medio](https://cienciatoday.com/volumen-plaquetario-medio/)
* [Triglirecidos](https://medlineplus.gov/spanish/triglycerides.html)
* [High triglycerides](https://www.webmd.com/cholesterol-management/tc/high-triglycerides-overview)