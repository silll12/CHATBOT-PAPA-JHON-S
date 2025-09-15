# -*- coding: utf-8 -*-

import re
import time
from datetime import datetime

# -------------------------
# Expresiones regulares
# -------------------------
# Promociones / cupones
PROMO_RE = r"\b(promo(?:ciones)?|descuento(s)?|oferta(s)?|cup(o|ó)n(es)?)\b"

# Hacer pedido (intención general de ordenar)
PEDIDO_RE = r"\b(pedir|orden(ar|ar)|quiero (una|la)? pizza|hacer un pedido|comprar pizza|me antoja (una )?pizza)\b"

# Tipo de servicio: Domicilio vs. Recoger en tienda
ENTREGA_RE = r"\b(entrega(:?s))"
DOMICILIO_RE = r"\b(a (domicilio|casa)|entrega(r)?|env(í|i)o|llevar a mi casa|reparto|delivery)\b"
RECOGER_RE  = r"\b(recoger|para llevar|pick(\s|-)?up|paso por (ella|mi pedido)|ir por mi pedido)\b"

# Sucursal / ubicación cercana
SUCURSAL_RE = r"\b(sucursal(es)?|tienda(s)?|ubicaci(ó|o)n|dónde (están|quedan)|cerca (de m[ií]|aquí))\b"

# Horarios / apertura
HORARIO_RE = r"\b(horario(s)?|a qu(e|é) hora(s)? (abren|cierran)|est(á|a)n (abiertos|cerrados) (hoy|ahora)?)\b"

# Menú / carta
MENU_RE = r"\b(men(ú|u)|carta|sabores|especialidades|pizzas disponibles|ingrediente(s)?)\b"

# Estado de pedido / seguimiento
ESTADO_PEDIDO_RE = r"\b(estado (de )?mi pedido|seguimiento|track(ear)?|d(ó|o)nde va mi pedido)\b"

#Ver Método de pago
VER_METODO_PAGO_RE = r"\b(metodo(s)? de pago(s)?|pago(s)?|pagar|efectivo(s)?|tarjeta(s)?|visa(s)?|mastercard(s)?|american express(s?))\b"

# Método de pago
METODO_PAGO_RE = r"\b(metodo(s)? de pago(s)?|pago(s)?|pagar|efectivo(s)?|tarjeta(s)?|visa(s)?|mastercard(s)?|american express(s?))\b"

TARJETA_RE = r"\b(tarjeta(s)?|visa(s)?|mastercard(s)?|american express(s?))"
BRAND_RE = r"^(visa|mastercard|american express|amex|carnet)$"
EXP_RE = r"^(0[1-9]|1[0-2])\/\d{2}$"   # MM/AA
LAST4_RE = r"^\d{4}$"

# Afirmaciones / confirmaciones
AFIRMACION_RE = r"\b(s[ií]|claro|por supuesto|correcto|perfecto|de acuerdo|ok|vale|sí por favor)\b"

# Negaciones / correcciones       #También se puede agregar "quit(a|ar)"#
NEGACION_RE = r"\b(no|mejor no|cancela|cambiar|no es as[ií]|eso no|negar)\b"

# Salir / terminar conversación
SALIR_RE = r"\b(salir|ad(i|í)os|gracias(,? ad(i|í)os)?|terminar|hasta luego|nos vemos)\b"

# Ayuda
AYUDA_RE = r"\b(ayuda|necesito ayuda|no entiendo|opciones|men(ú|u) de ayuda)\b"

# Contacto
CONTACTO_RE = r"\b(?:contacto|comunica(?:r(?:se)?)?|hablar (?:con|a)? (?:alguien|un operador|un agente)|atenci(?:ó|o)n(?: al cliente)?|soporte|queja(?:s)?|reclamo(?:s)?|ayuda (?:humana|en vivo)|llamar)\b"

# Peticiones fuera de contexto
EXTRA_RE = r"\b(escrib(e|ir))\b"

regex_menu = {
    r"hawaiana": "Hawaiana Pizza de jamón, piña y extra queso 100% Mozzarella.",
    r"super\s*pe+per?on+i": "Super Pepperoni Pizza con extra porción de pepperoni y extra queso.",
    r"vegetarian[ao]": "Pizza con vegetales frescos: champiñones, cebolla, pimiento verde, jitomate y aceitunas negras",
    r"mexican[ao]": "Pizza con chorizo, carne de res, cebolla, jalapeños picositos y salsa de tomate con frijoles.",
    r"caribeñ[ao]": "Pizza con piña y chile molido",
    r"the\s*works": "The Works Pizza de pepperoni, salchicha italiana, jamón, champiñones, cebolla, pimiento verde y aceitunas negras",
    r"papas?\s*favorite": "Papas Favorite Pizza con mezcla de 6 quesos (Mozzarella, Parmesano, Romano, Asiago, Fontina, Provolone), pepperoni, salchicha de cerdo",
    r"all\s*the\s*meats": "All The Meats Pizza con carnes frías: pepperoni, salchicha de puerco, carne de res, jamón y tocino",
    r"pe+per?on+i\s*xl\s*masa\s*delgada": "Nuestra pizza Pepperoni XL es extra grande en sabor.",
    r"arma\s*tu\s*pizza": "Elige el tamaño, la masa y luego añade tus ingredientes favoritos y nosotros la haremos por ti.",
    r"mitad\s*y\s*mitad": "Te pasa que a veces no puedes decidir? Pues esta es definitivamente para ti. Dos sabores en una sola pizza, perfecta para cuando tienes antojo de dos sabores.",
    r"tuscan\s*six\s*cheese": "Tuscan Six Cheese Pizza con mezcla de 6 quesos: Mozzarella, Parmesano, Romano, Asiago, Fontina, Provolone y hierbas italianas.",
    # Complementos

    r"mini\s*cheesesticks": "Mini Cheesesticks con queso fundido y masa doradita.",
    r"pepperoni\s*rolls": "Pepperoni Rolls rellenos de pepperoni y queso mozzarella.",
    r"potato\s*wedges": "Papas gajo sazonadas y doradas al horno.",
    r"calzone\s*jam[oó]n\s*y\s*piñ[ae]": "Calzone relleno de jamón y piña con queso derretido.",
    r"calzone\s*jam[oó]n\s*y\s*champ[ií]ñones": "Calzone con jamón y champiñones frescos.",
    r"calzone\s*pe+per?on+i": "Calzone relleno de pepperoni y queso fundido.",

    # postres
    r"snickers\s*rolls": "Deliciosos Snickers® Rolls con relleno cremoso.",
    r"milky\s*way\s*rolls": "Milky Way® Rolls rellenos de chocolate y caramelo.",
    r"chocoavellana\s*pay": "Pay relleno de chocoavellana y cubierta de chocolate.",
    r"chocoavellana\s*snickers": "Postre de chocoavellana con Snickers®.",
    r"chocoavellana\s*milky\s*way": "Postre de chocoavellana con Milky Way®.",
    r"chocoavellana\s*m&m'?s": "Postre de chocoavellana con M&M'S®.",

    # bebidas
    r"coca\s*cola\s*2l?t": "Coca Cola 2lt bien fría.",
    r"coca\s*cola\s*light\s*2l?t": "Coca Cola Light 2lt para los que prefieren menos calorías.",
    r"sidral\s*2l?t": "Sidral 2lt refrescante y dulce.",
    r"fanta\s*2l?t": "Fanta Naranja 2lt burbujeante.",
    r"sprite\s*2l?t": "Sprite 2lt sabor limón.",
    r"fresca\s*2l?t": "Fresca 2lt sabor toronja.",
    r"coca\s*cola\s*lata\s*355ml": "Coca Cola en lata 355ml.",
    r"coca\s*cola\s*sin\s*az[uú]car\s*lata\s*355ml": "Coca Cola sin azúcar en lata 355ml.",
    r"coca\s*cola\s*light\s*lata\s*355ml": "Coca Cola Light en lata 355ml.",
    r"sidral\s*mundet\s*lata\s*355ml": "Sidral Mundet en lata 355ml.",
    r"fanta\s*naranja\s*lata\s*355ml": "Fanta Naranja en lata 355ml.",
    r"sprite\s*lata\s*355ml": "Sprite en lata 355ml.",
    r"fresca\s*toronja\s*lata\s*355ml": "Fresca Toronja en lata 355ml.",
    r"delaware\s*punch\s*lata\s*355ml": "Delaware Punch en lata 355ml.",
    r"fuze\s*tea\s*verde\s*lim[oó]n\s*600ml": "Fuze Tea verde limón 600ml.",
    r"fuze\s*tea\s*negro\s*lim[oó]n\s*600ml": "Fuze Tea negro limón 600ml.",
    r"fuze\s*tea\s*negro\s*durazno\s*600ml": "Fuze Tea negro durazno 600ml.",
    r"agua\s*ciel\s*600ml": "Agua Ciel natural 600ml.",
    r"agua\s*ciel\s*jam[aá]ica\s*600ml": "Agua Ciel Jamaica 600ml.",
    r"agua\s*ciel\s*lim[oó]n\s*600ml": "Agua Ciel Limón 600ml.",

    # extra
    r"dip\s*salsa\s*bbq": "Dip Salsa BBQ para acompañar tu pizza.",
    r"dip\s*salsa\s*de\s*ajo": "Dip Salsa de Ajo cremosa.",
    r"peperoncini": "Peperoncini picantes para los valientes."
}



def main():
    state = 0
    Salida = 1
    name = ""  # para evitar referencia antes de asignación

    while Salida:
        if state == 0:
            print("Hola soy el Chatbot de Papa John's ¿En qué te puedo ayudar?")
            time.sleep(1)
            opcion = input("Soy capaz de informarte de nuestras promociones, ayudarte a ordenar pizza, encontrar sucursales, nuestros horarios, nuestro menús, estado de tu pedido, nuestros contactos. \n\t\t\t")
            if re.findall(PROMO_RE, opcion, re.IGNORECASE):
                state = 1
            elif re.findall(PEDIDO_RE, opcion, re.IGNORECASE):
                state = 2
            elif re.findall(ENTREGA_RE, opcion, re.IGNORECASE) \
                or re.findall(DOMICILIO_RE, opcion, re.IGNORECASE) \
                or re.findall(RECOGER_RE, opcion, re.IGNORECASE):
                state = 3
            elif re.findall(SUCURSAL_RE, opcion, re.IGNORECASE):
                state = 4
            elif re.findall(HORARIO_RE, opcion, re.IGNORECASE):
                state = 5
            elif re.findall(MENU_RE, opcion, re.IGNORECASE):
                state = 6
            elif re.findall(ESTADO_PEDIDO_RE, opcion, re.IGNORECASE):
                state = 7
            elif re.findall(VER_METODO_PAGO_RE, opcion, re.IGNORECASE):
                state = 8
            elif re.findall(AFIRMACION_RE, opcion, re.IGNORECASE):
                state = 9
            elif re.findall(NEGACION_RE, opcion, re.IGNORECASE):
                state = 10
            elif re.findall(AYUDA_RE, opcion, re.IGNORECASE):
                state = 12
            elif re.findall(CONTACTO_RE, opcion, re.IGNORECASE):
                state = 13
            elif re.findall(SALIR_RE, opcion, re.IGNORECASE):
                state = 11
            else:
                state = 30

        if state == 1:
            opcion = input(
                " Nuestras promociones del momento son:\n"
                "- Especialidades a $159.\n"
                "- Pizza especial con un postre de $49.\n"
                "- Pizza signature con un postre de $49.\n"
                "- Pizza especial con un regresco de 2L de $40.\n"
                "- Pizza signature con un refresco de 2L de $40.\n"
                "- Papa Combo $195.\n"
                "- Star Pizza $239.\n"
                "- Combo404 $404.\n"
                "- Pizza en forma de corazón a $219\n"
                "- Paquete corazón a $299\n\n"
                "¿Desea ordenar alguna promoción? "
            )
            time.sleep(0.3)
            if re.search(AFIRMACION_RE, opcion, re.IGNORECASE):
                state = 2
            else:
                state = 0

        if state == 2: #Aun sigo en esta :)
            print("Muchas gracias por ordenar con nosotros \n")
            respuesta=input("Dime si empezamos con tu pedido o puedo mostrarte nuestro menu \n")

            if re.search(MENU_RE, respuesta,re.IGNORECASE):
                state = 6
            elif re.search(PEDIDO_RE, respuesta, re.IGNORECASE):
                print("Perfecto, empezemos con las pizzas")
                pedido_pizza=input("Que pizza te gustaria para ordenar?")

                if re.search(pedido_pizza,NEGACION_RE,re.IGNORECASE):
                    pedido_extra= input("Oh, Dime que te gustaria ordenar de nuestra area de bebidas y postres")
                masdeuna=input("Seria todo de nuestra area de pizzas?, puedo ofrecerte nuestras promociones\n"
                                "Nuestras promociones del momento son:\n"
                                "- Especialidades a $159.\n"
                                "- Pizza especial con un postre de $49.\n"
                                "- Pizza signature con un postre de $49.\n"
                                "- Pizza especial con un regresco de 2L de $40.\n"
                                "- Pizza signature con un refresco de 2L de $40.\n"
                                "- Papa Combo $195.\n"
                                "- Star Pizza $239.\n"
                                "- Combo404 $404.\n"
                                "- Pizza en forma de corazón a $219\n"
                                "- Paquete corazón a $299\n\n"
                                "¿Desea ordenar alguna promoción? ")

                if re.search(masdeuna,NEGACION_RE,re.IGNORECASE):
                    pedido_bebidadopostre=input("Entonces continuemos, te muestro nuestra seccion de bebidas y postres o seria todo?\n")
                    if re.search(pedido_bebidadopostre,FINALIZAR_RE, re.IGNORECASE):
                        print("Perfecto, entonces te muestro tu pedido, dime si esta todo correcto: \n")
                        print(f"Pedido: Pizza:{pedido_pizza}")
         #AYUDA
        if state == 12:
            print("\n=== Ayuda Papa John's ===")
            print("Puedes pedirme información sobre:")
            print("- Promociones")
            print("- Pedidos")
            print("- Sucursales")
            print("- Horarios")
            print("- Menú")
            print("- Estado de pedido")
            print("- Contacto")
            print("\nEjemplo de consulta: 'Quiero hacer un pedido' o 'Mostrar promociones'")

            input("\nPresiona Enter para volver al menú principal...")
            state = 0  # Regresamos al menú principal

        #CONTACTO
        if state == 13:
            while True:
                print("\n=== Soporte Papa John's ===")
                print("1) Teléfonos y correo")
                print("2) Queja o sugerencia")
                print("3) Rastreo de pedido (simulado)")
                print("Escribe 'menu' para volver al inicio.")

                op = input("Elige una opción: ").strip().lower()

                if op == "1":
                     print("📞 800 111 11 11  |  ✉️ soporte@papajohns.com")
                elif op == "2":
                    detalle = input("Cuéntanos tu queja o sugerencia: ")
                    print("Gracias, la canalizaremos a nuestro equipo.")
                elif op == "3":
                    pid = input("Ingresa tu ID de pedido: ")
                    print(f"Pedido {pid}: en preparación (ejemplo).")
                elif op == "menu":
                    print("Regresando al menú principal.")
                    state = 0
                    break
                elif re.search(SALIR_RE, op, re.IGNORECASE):
                    print("¡Hasta luego!")
                    state = 11
                    break
                else:
                    print("Opción no válida. Intenta de nuevo.")
    
        #Horarios de las sucursales
        if state == 5:
            print("¡Claro! El horario de todas nuestras sucursales es el siguiente: \n"
            " - Lunes 11a.m. - 11p.m. \n"
            " - Martes 11a.m. - 11p.m. \n"
            " - Miércoles 11a.m. - 11p.m. \n"
            " - Jueves 11a.m. - 11p.m. \n"
            " - Viernes 11a.m. - 12a.m. \n"
            " - Sábado 11a.m. - 12a.m. \n"
            " - Domingo 11a.m. - 11p.m. \n")
            while True:
              sucursal = input("¿Quieres buscar una sucursal por tu zona? (sí/no): ").strip().lower()

              # salir / finalizar
              if re.search(SALIR_RE, sucursal, re.IGNORECASE):
                  state = 11
                  break

              # afirmación -> ir a búsqueda de sucursal
              if re.search(AFIRMACION_RE, sucursal, re.IGNORECASE):
                  state = 4
                  print("Para localizar tu tienda más cercana es necesario que indiques en qué alcadía te encuentras")
                  break

              # negación -> volver al menú principal
              if re.search(NEGACION_RE, sucursal, re.IGNORECASE):
                  print("Serás redirigido al menú principal.")
                  state = 0
                  break

              # cualquier otra cosa -> volver a preguntar
              print("Respuesta inválida. Escribe 'sí' o 'no'.")

        if state == 6:
            print("Bienvenido al menú de Papa John's, espero encuentres lo que buscas \n"
                  " *Pizzas: \n"
                  "   - Arma tu pizza \n"
                  "   - Mitad y Mitad \n"
                  "   - Hawaiana \n"
                  "   - Super peperoni \n"
                  "   - Tuscan Six Cheese \n"
                  "   - Vegetariana \n"
                  "   - Mexicana \n"
                  "   - Caribeña \n"
                  "   - The Works \n"
                  "   - Papas Favorite \n"
                  "   - All The Meats \n"
                  "   - Peperoni XL Masa Delgada \n"
                  " *Complementos\n"
                  "   - Mini Cheesesticks\n"
                  "   - Pepperoni Rolls\n"
                  "   - Potato Wedges\n"
                  "   - Calzone jamón y piña\n"
                  "   - Calzone jamón y champiñones\n"
                  "   - Calzone pepperoni\n"
                  " *Postres\n"
                  "   - Snickers® Rolls\n"
                  "   - Milky Way® Rolls\n"
                  "   - Chocoavellana Pay\n"
                  "   - Chocoavellana Snickers®\n"
                  "   - Chocoavellana Milky Way®\n"
                  "   - Chocoavellana M&M'S®\n"
                  " *Bebidas\n"
                  "   - Coca Cola 2lt\n"
                  "   - Coca Cola light 2lt\n"
                  "   - Sidral 2Lt\n"
                  "   - Fanta 2lt\n"
                  "   - Sprite 2lt\n"
                  "   - Fresca 2lt\n"
                  "   - Coca Cola lata 355ml\n"
                  "   - Coca Cola sin azúcar lata 355ml\n"
                  "   - Coca Cola light lata 355ml\n"
                  "   - Sidral Mundet lata 355ml\n"
                  "   - Fanta naranja lata 355ml\n"
                  "   - Sprite lata 355ml\n"
                  "   - Fresca Toronja Lata 355 ML\n"
                  "   - Delaware Punch lata 355ml\n"
                  "   - Fuze Tea verde limón 600ml\n"
                  "   - Fuze Tea negro limón 600ml\n"
                  "   - Fuze Tea negro durazno 600ml\n"
                  "   - Agua Ciel 600ml\n"
                  "   - Agua Ciel Jamaica 600ml\n"
                  "   - Agua Ciel Limón 600ml\n"
                  " *Extras\n"
                  "   - Dip Salsa BBQ\n"
                  "   - Dip Salsa de Ajo\n"
                  "   - Peperoncini\n"
                  "Escribe el nombre de la pizza que deseas, o 'salir' para terminar.")

            while True:  # Mantenerse en el menú hasta que elija algo o salga
                opcion_pizza = input("Tu elección: ").strip()

                #Si el usuario llega a querer salir del menu
                if re.search(SALIR_RE, opcion_pizza, re.IGNORECASE):
                    state = 11
                    break

                # Buscar la pizza con las expresiones regulares
                encontrada = None
                for patron, descripcion in regex_menu.items():
                    if re.search(patron, opcion_pizza, re.IGNORECASE):
                        encontrada = (patron, descripcion)
                        break

                if encontrada:
                    print(f"La pizza: {opcion_pizza.title()}")
                    print(f"{encontrada[1]}")
                    pedido= input("Te gustaria pasar a relizar tu pedido o te si gustas puedes seguir navegando por el menu \n")
                    if re.search(MENU_RE,pedido,re.IGNORECASE):
                        break
                    elif re.search(PEDIDO_RE,pedido,re.IGNORECASE):
                        state = 2  # Redireccionamos al estado de pedido
                        break

                else:
                    print("No entendí tu elección. Intenta con el nombre de una pizza o 'salir'.")

        #Métodos de pagos por si solo el cliente quiere saberlos
        if state == 8:
            opcion = input("Nuestros métodos de pago disponibles son: \n"
                "- Efectivo \n"
                "- Tarjeta (American Express / Carnet / Mastercad / Visa) \n"
                "- Trabajamos con los siguiente bancos: \n"
                "  - AFIRME \t\t - Inbursa \n"
                "  - Banco Azteca \t - Invex \n"
                "  - Banorte \t\t - Ixe \n"
                "  - BanRegio \t\t - Monex \n"
                "  - BBVA \t\t - Santander \n"
                "  - Citibanamex \t - Scotiabank \n"
                "  - HSBC \n"
                "¿Quisiera ordenar algo? \n"
            )
            if re.findall(SALIR_RE, opcion, re.IGNORECASE):
              state = 11

            if re.findall(AFIRMACION_RE, opcion, re.IGNORECASE):
              state = 6

            if re.findall(NEGACION_RE, opcion, re.IGNORECASE):
              print("Serás redirigido al menú principal.")
              state = 0

        #Métodos de pago que se le mostrarán al cliente cuando este apunto de pagar su orden
        if state == 14:
            opcion = input("Nuestros métodos de pago disponibles son: \n"
                "- Efectivo \n"
                "- Tarjeta (American Express / Carnet / Mastercad / Visa) \n"
                "- Trabajamos con los siguiente bancos: \n"
                "  - AFIRME \t\t - Inbursa \n"
                "  - Banco Azteca \t - Invex \n"
                "  - Banorte \t\t - Ixe \n"
                "  - BanRegio \t\t - Monex \n"
                "  - BBVA \t\t - Santander \n"
                "  - Citibanamex \t - Scotiabank \n"
                "  - HSBC \n"
                "¿Qué método de pago quiere usar, efectivo o tarjeta? \n"
            )
            if re.findall(SALIR_RE, opcion, re.IGNORECASE):
              state = 11
            elif re.findall(TARJETA_RE, opcion, re.IGNORECASE):
              state = 14
            else:
              state = 15

        if state == 11:
          print("¡Gracias! Fue un placer atenderte. 👋")
          Salida = 0

        if state == 14:
            print("Perfecto. Para pagos con tarjeta NO solicitamos datos sensibles.")
            print("Por seguridad, solo recopilaremos: marca de tarjeta, nombre del titular, últimos 4 dígitos y vigencia (MM/AA).")

            # Marca
            while True:
                marca = input("Marca de la tarjeta (Visa / Mastercard / American Express / Carnet): ").strip().lower()
                marca_normalizada = (
                    "american express" if re.search(r"^(american\s*express|amex)$", marca) else
                    "mastercard" if re.search(r"^master(card)?$", marca) else
                    marca
                )
                if re.match(BRAND_RE, marca_normalizada):
                    break
                print("Marca no válida. Intente con: Visa, Mastercard, American Express o Carnet.")
                if re.findall(SALIR_RE, marca, re.IGNORECASE):
                  state = 11
                  break
                if re.search(NEGACION_RE, marca, re.IGNORECASE):
                  print("Serás redirigido al menú principal.")
                  state = 0
                  break


            # Nombre del titular
            while True:
                titular = input("Nombre del titular (como aparece en la tarjeta): ").strip()
                if len(titular) >= 3:
                    break
                print("Ingrese un nombre válido (3+ caracteres).")
                if re.findall(SALIR_RE, titular, re.IGNORECASE):
                  state = 11
                  break
                if re.search(NEGACION_RE, titular, re.IGNORECASE):
                  print("Serás redirigido al menú principal.")
                  state = 0
                  break

            # Últimos 4 dígitos
            while True:
                ult4 = input("Ingresa SOLO los últimos 4 dígitos de la tarjeta: ").strip()
                if re.match(LAST4_RE, ult4):
                    break
                print("Deben ser exactamente 4 dígitos.")
                if re.findall(SALIR_RE, ult4, re.IGNORECASE):
                  state = 11
                  break
                if re.search(NEGACION_RE, ult4, re.IGNORECASE):
                  print("Serás redirigido al menú principal.")
                  state = 0
                  break

            # Vigencia MM/AA
            while True:
                vigencia = input("Vigencia (MM/AA): ").strip()
                if re.match(EXP_RE, vigencia):
                    # Validación básica de fecha no expirada (opcional)
                    try:
                        mm, aa = vigencia.split("/")
                        mm = int(mm)
                        aa = int("20" + aa)  # asume 20AA
                        ahora = datetime.now()
                        # Considera válida si el último día del mes aún no pasó
                        if (aa > ahora.year) or (aa == ahora.year and mm >= ahora.month):
                            break
                        else:
                            print("La tarjeta parece estar vencida. Verifique la vigencia.")
                    except Exception:
                        print("Formato inválido. Use MM/AA (ej. 07/27).")
                else:
                    print("Número de mes inválido.")
                if re.findall(SALIR_RE, vigencia, re.IGNORECASE):
                  state = 11
                  break
                if re.search(NEGACION_RE, vigencia, re.IGNORECASE):
                  print("Serás redirigido al menú principal.")
                  state = 0
                  break

            print(f"\nDatos recibidos:")
            print(f"- Marca: {marca_normalizada.title()}")
            print(f"- Titular: {titular}")
            print(f"- Terminación: **** {ult4}")
            print(f"- Vigencia: {vigencia}")
            print("El cobro se ha realizado correctamente, será redirigido al menú principal. ✅\n")
            time.sleep(0.5)
            state = 0

        if state == 15:
            necesita = input("¡Perfecto! ¿Necesitará cambio o pagará exacto? ").strip().lower()
            if re.search(r"\b(cambio|sí|si|por favor|claro|ok|vale)\b", necesita):
                while True:
                    para = input("¿Para cuánto (monto numérico)? ").strip().replace(",", "")
                    try:
                        monto = float(para)
                        print(f"Anotado: se llevará cambio para ${monto:,.2f}. ✅\n")
                        break
                    except ValueError:
                        print("Monto inválido. Intente de nuevo.")
            else:
                print("Perfecto, se registró pago exacto. ✅\n")
            state = 0  # volver al menú principal
            if re.findall(SALIR_RE, necesita, re.IGNORECASE):
                  state = 11
                  break
            if re.search(NEGACION_RE, necesita, re.IGNORECASE):
                  print("Serás redirigido al menú principal.")
                  state = 0
                  break

        # Caso default para cualquier otra petición
        # Aún sin terminar
        if state == 30:
          if re.findall(EXTRA_RE, opcion, re.IGNORECASE):
            print(f"Discupa, pero no soy capaz {opcion}")
            print("¡Pero puedes preguntar acerca de pizzas!")
            state = 0
          else:
            print("Waos")
            state = 0

          ##print("Hmmm")
          ##time.sleep(1)
          ##print("Lo siento, no puedo ayudarte con eso")
          ##print("Pero sí se trata de una de una pizza, entonces ¡soy el indicado! 🤗")



if __name__ == "__main__":
    main()
