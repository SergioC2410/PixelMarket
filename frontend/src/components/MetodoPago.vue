<template>
  <div class="payment-methods">
    <h2>Selecciona tu método de pago</h2>
    <div class="accordion">
      <div v-for="method in paymentMethods" :key="method.id" class="accordion-item">
        <div class="accordion-header" @click="toggleAccordion(method.id)">
          <img :src="method.icon" :alt="method.name" class="method-icon" />
          <span>{{ method.name }}</span>
        </div>
        <div v-if="activeMethod === method.id" class="accordion-content">
          <p>{{ method.description }}</p>
          <button @click="selectMethod(method)" class="select-btn">Seleccionar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      activeMethod: null,
      paymentMethods: [
        {
          id: 1,
          name: 'Pago Móvil',
          description: 'Paga con tu banco nacional al instante.',
          icon: require('@/assets/img-pagos/vepagomovilc2c.png'), // Ruta relativa
        },
        {
          id: 2,
          name: 'zelle',
          description: 'Paga con tu banco internacional al instante.',
          icon: require('@/assets/img-pagos/usa-zelle-c.png'),
        },
        {
          id: 3,
          name: 'Binance',
          description: 'Paga con tus Usdt desde cualquier parte del mundo.',
          icon: require('@/assets/img-pagos/ven-binance.png'),
        },
        {
          id: 4,
          name: 'Cash',
          description: 'paga en efectivo.',
          icon: '   https://cdn-icons-png.flaticon.com/512/1052/1052866.png ',
        },
      ],
    };
  },
  methods: {
    toggleAccordion(methodId) {
      this.activeMethod = this.activeMethod === methodId ? null : methodId;
    },
    selectMethod(method) {
      alert(`Método seleccionado: ${method.name}`);
    },
  },
};
</script>

<style scoped>
.payment-methods {
  padding: 1.5rem;
  background-color: #ffff;
  border-radius: 10px;
  max-width: 600px;
  margin: 0 auto;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  margin: 2rem auto
}

h2 {
  text-align: center;
  margin-bottom: 2rem;
  font-size: 1.5rem;
  color: #333;
}

.accordion-item {
  background-color: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  margin-bottom: 1rem;
  overflow: hidden;
}

.accordion-header {
  display: flex;
  align-items: center;
  padding: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.accordion-header:hover {
  background-color: #f0f0f0;
}

.method-icon {
  width: 30px;
  height: 30px;
  margin-right: 1rem;
}

.accordion-content {
  padding: 1rem;
  border-top: 1px solid #e0e0e0;
}

.select-btn {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.select-btn:hover {
  background-color: #0056b3;
}
</style>