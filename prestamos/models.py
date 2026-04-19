from django.db import models

class Cliente(models.Model):
    cedula = models.CharField(max_length=20, primary_key=True)
    nombre = models.CharField(max_length=100)
    celular = models.CharField(max_length=15)
    direccion = models.CharField(max_length=300)

    # Llaves Foráneas (FK) - Relaciones
    #En esta no pongo "id" porque django lo pone al final
    referencia = models.ForeignKey(
        'Referencia',
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'Cliente'


class Referencia(models.Model):
    cedula = models.CharField(max_length=20, primary_key=True)
    nombre = models.CharField(max_length=100)
    celular = models.CharField(max_length=15)
    direccion = models.CharField(max_length=300)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'Referencia'

class Metodo_de_pago(models.Model):
    id_metodo_pago = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'MetodoDePago'



class Estado(models.Model):
    id_estado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'Estado'


class FrecuenciaPago(models.Model):
    id_frecuencia_pago = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20)
    dias = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'FrecuenciaPago'


class Credito(models.Model):
    id_credito = models.AutoField(primary_key=True)
    monto_de_prestamo = models.DecimalField(max_digits=12, decimal_places=2)
    interes = models.DecimalField(max_digits=4, decimal_places=2)
    n_cuotas = models.IntegerField() 
    fecha_prestamo = models.DateTimeField()
    fecha_limite = models.DateField()

    # Llaves Foráneas (FK) - Relaciones 
    #si borro una frecuencia no se me va a borrar el credito. 
    frecuencia = models.ForeignKey(FrecuenciaPago, on_delete=models.SET_NULL,
        null=True)
    
    #si borro un cliente, se van a borrar sus creditos. 
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return f"Credito {self.id_credito}"

    class Meta:
        db_table = 'Credito'


class Cuota(models.Model):
    
    id_cuota = models.AutoField(primary_key=True)
    numero_de_cuota = models.IntegerField()
    fecha_esperada = models.DateField()
    fecha_pago_real = models.DateTimeField(null=True, blank=True) # null=True porque al inicio no se ha pagado
    monto_capital = models.DecimalField(max_digits=12, decimal_places=2)
    monto_intereses = models.DecimalField(max_digits=12, decimal_places=2)
    monto_total = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Llaves Foráneas (FK) - Relaciones
    #El estado protect va a evitar que se borre un estado si hay cuotas usandolo. 
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT)
    credito = models.ForeignKey(Credito, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cuota {self.id_cuota}"
    
    class Meta:
        db_table = 'Cuota'


class Abono(models.Model):
    
    id_abono = models.AutoField(primary_key=True)
    numero_de_cuota = models.IntegerField()
    fecha_pago = models.DateField()
    monto_total = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Llaves Foráneas (FK) - Relaciones
    metodo_de_pago = models.ForeignKey(Metodo_de_pago, on_delete=models.PROTECT)
    cuota = models.ForeignKey('Cuota', on_delete=models.CASCADE)
    credito = models.ForeignKey('Credito', on_delete=models.CASCADE)

    def __str__(self):
        return f"Abono {self.id_abono}"
    
    class Meta:
        db_table = 'Abono'
