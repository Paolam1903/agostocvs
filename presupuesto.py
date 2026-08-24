import pandas as pd

# =====================
# REGLA DE DISTRIBUCIÓN
# =====================
def calcular_distribucion(n_asesores, cvs, nombre=None, rol=None):

    cvs = str(cvs).upper()
    nombre = str(nombre).upper() if nombre else ""
           
    # ==================================================
    # 🔴 REGLA ESPECIAL FRONTINO
    # ==================================================
    if cvs == "FRONTINO":
        if rol == "LIDER":
            return 0.50
        else:
            return 0.50


    # ==================================================
    # NECHI
    # ==================================================

    if cvs == "NECHI":

        # Lider Nechi Maricela
        if rol == "LIDER":
            return 300 / 2000

        # LeidisÂ  Rosa
        elif "LEIDISÂ" in nombre:
            return 1700 / 2000


    # ==================================================
    # CIUDAD BOLIVAR
    # ==================================================

    if cvs == "CIUDAD BOLIVAR":

        # Lider Natalie
        if rol == "LIDER":
            return 1087.5 / 1500

        # Leidy Yaneth
        elif "LEIDY" in nombre:
            return 412.5 / 1500

    # ==================================================
    # EL BAGRE
    # ==================================================

    if cvs == "EL BAGRE":

        # Líder
        if rol == "LIDER":
            return 1006 / 3500

        # Darly
        elif "DARLY" in nombre:
            return 1509 / 3500

        # Jeider
        elif "JEIDER" in nombre:
            return 985 / 3500

    # ==================================================
    # ENVIGADO
    # ==================================================

    if cvs == "ENVIGADO":

        # Líder
        if rol == "LIDER":
            return 1159.5 / 3500

        # Yessica
        elif "YESSICA" in nombre:
            return 1739 / 3500

        # Luz Enith
        elif "LUZ" in nombre:
            return 601.5 / 3500     

    # ==================================================
    # SABANETA
    # ==================================================

    if cvs == "SABANETA":

        # LÃ­der Sandra - 40%
        if rol == "LIDER":
            return 1040 / 2600

        # Andrea - 11 días
        elif "ANDREA" in nombre:
            return 715 / 2600

        # Luz - 13 días
        elif "LUZ" in nombre:
            return 845 / 2600  


    # ==================================================
    # CALDAS
    # ==================================================
    if cvs == "CALDAS":

        # Líder Yolima
        if rol == "LIDER":
            return 1202 / 3700

        # Darinela
        elif "DARINELA" in nombre:
            return 694 / 3700

        # Johnson
        elif "JOHNSON" in nombre:
            return 1804 / 3700
    
    # ==================================================
    # 🔴 REGLAS NORMALES
    # ==================================================

    # Si no hay asesores
    if n_asesores == 0:
        return 1.0

    if rol == "LIDER":

        if n_asesores == 1:
            return 0.40
        elif n_asesores == 2:
            return 0.25
        elif n_asesores >= 3:
            return 0.20

    else:

        if n_asesores == 1:
            return 0.60
        elif n_asesores == 2:
            return 0.375
        elif n_asesores >= 3:
            return 0.266

    return 1.0


# =================================================
# META GENERAL + EJECUCIÓN (RESUMEN POR CVS)
# =================================================
def resumen_meta_general_por_cvs(df):
    resultados = []

    for sucursal, grupo in df.groupby("Sucursal"):
        meta_total = grupo["Meta_General"].iloc[0]

        n_asesores = grupo[grupo["Rol"] == "ASESOR"]["Cedula_Vendedor"].nunique()
        pct_lider, pct_asesores = calcular_distribucion(n_asesores, sucursal)


        puntos_lider = grupo[grupo["Rol"] == "LIDER"]["Puntos"].sum()
        puntos_asesores = grupo[grupo["Rol"] == "ASESOR"]["Puntos"].sum()

        resultados.append({
            "Sucursal": sucursal,
            "Estructura": f"1 Líder + {n_asesores} Asesor(es)",

            "Meta CVS": meta_total,

            "Meta Líder": meta_total * pct_lider,
            "Ejecutado Líder": puntos_lider,
            "Cumplimiento Líder %": round(
                (puntos_lider / (meta_total * pct_lider)) * 100, 2
            ) if meta_total * pct_lider > 0 else 0,

            "Meta Asesores": meta_total * pct_asesores,
            "Ejecutado Asesores": puntos_asesores,
            "Cumplimiento Asesores %": round(
                (puntos_asesores / (meta_total * pct_asesores)) * 100, 2
            ) if meta_total * pct_asesores > 0 else 0,
        })

    return pd.DataFrame(resultados)


# =================================================
# KPI POR PRODUCTO + EJECUCIÓN (RESUMEN POR CVS)
# =================================================
def resumen_kpi_producto_por_cvs(df):
    resultados = []

    for (sucursal, producto), grupo in df.groupby(["Sucursal", "Producto"]):
        meta_producto = grupo["Meta_Producto"].iloc[0]

        n_asesores = grupo[grupo["Rol"] == "ASESOR"]["Cedula_Vendedor"].nunique()
        pct_lider, pct_asesores = calcular_distribucion(n_asesores, sucursal)


        puntos_lider = grupo[grupo["Rol"] == "LIDER"]["Puntos"].sum()
        puntos_asesores = grupo[grupo["Rol"] == "ASESOR"]["Puntos"].sum()

        resultados.append({
            "Sucursal": sucursal,
            "Producto": producto,

            "Meta Producto": meta_producto,

            "Meta Líder": meta_producto * pct_lider,
            "Ejecutado Líder": puntos_lider,
            "Cumplimiento Líder %": round(
                (puntos_lider / (meta_producto * pct_lider)) * 100, 2
            ) if meta_producto * pct_lider >= 0 else 0,

            "Meta Asesores": meta_producto * pct_asesores,
            "Ejecutado Asesores": puntos_asesores,
            "Cumplimiento Asesores %": round(
                (puntos_asesores / (meta_producto * pct_asesores)) * 100, 2
            ) if meta_producto * pct_asesores >= 0 else 0,
        })

    return pd.DataFrame(resultados)
