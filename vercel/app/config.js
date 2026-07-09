// ============================================================
// CONFIGURACIÓN · Fiscalización Municipal · Coordenada Pública
// Compartida por la app (/app) y los visores comunales.
//
// PASO ÚNICO tras crear el proyecto Supabase (ver supabase/SUPABASE_SETUP.md):
//   1. Copiar "Project URL" y "anon public key" desde
//      Supabase → Settings → API
//   2. Pegarlas abajo y hacer git push.
//
// Si quedan vacías, la app funciona en MODO DEMO (almacenamiento
// local del dispositivo + export CSV compatible con el visor).
// ============================================================
window.FISCAL_CONFIG = {
  SUPABASE_URL: "",        // ej: "https://abcdefgh.supabase.co"
  SUPABASE_ANON_KEY: "",   // ej: "eyJhbGciOi..."

  // Parámetros operativos
  UTM_CLP: 72307,          // valor UTM (abril 2026) · actualizar mensualmente
  COMUNA_DEFAULT: "Estación Central",
  COMUNAS: [
    "Estación Central","Santiago","La Reina","Maipú","Ñuñoa","Peñaflor",
    "San Bernardo","Melipilla","La Florida","Puente Alto","San Joaquín",
    "Talagante","Paine","Padre Hurtado","La Pintana","Pirque","Lo Prado"
  ],

  // UTM/día por gravedad (Ordenanza tipo, rango 0 a 5 UTM)
  UTM_POR_GRAVEDAD: {
    "Sin infracción": 0,
    "Leve": 1,
    "Moderada (Abandono)": 3,
    "Grave (Riesgo Inminente)": 5
  },

  // Sondeo del visor (segundos)
  VISOR_POLL_S: 30
};
