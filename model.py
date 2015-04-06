import sqlite3
db = sqlite3.connect('redalert.db')
db = db.cursor()


class Get:
    @staticmethod
    def zone(zone_cat_id):
        if zone_cat_id == "null":
            return

        db.execute("""
            SELECT  zones.zone_id,
                    zones.zone_cat_id,
                    zones.input_cat_id,
                    zones.input_nc,
                    zones.output_cat_id,
                    zones.output_nc,
                    zones.output_timeout,
                    zones.output_timeout_nzone,
                    zones.input_cat_id_reset,
                    zones.input_cat_id_reset_nzone,
                    zones.time_reset,
                    zones.time_reset_nzone,
                    zone_categories.zone_cat_name,
                    zone_categories.zone_cat_alt_name
            FROM    zones
            INNER
            JOIN    zone_categories ON zones.zone_cat_id = zone_categories.zone_cat_id
            WHERE   zone_categories.zone_cat_id = %d
        """ % int(zone_cat_id))

        zz = []

        for data in db:
            if data[13]:
                cat_name = data[13]
            else:
                cat_name = data[12]

            z = {
                'zone_id': data[0],
                'zone_cat_id': data[1],
                'input_cat_id': data[2],
                'input_nc': data[3],
                'output_cat_id': data[4],
                'output_nc': data[5],
                'output_timeout': data[6],
                'output_timeout_nzone': data[7],
                'output_cat_id_reset': data[8],
                'output_cat_id_reset_nzone': data[9],
                'time_reset': data[10],
                'time_reset_nzone': data[11],
                'zone_name': cat_name
            }

            zz.append(z)

        return zz

    @staticmethod
    def input_cats(cat_id):
        if cat_id == "null":
            return

        db.execute("""
          SELECT  input_categories.input_cat_id,
                  input_categories.input_cat_name,
                  input_categories.input_cat_alt_name,
                  inputs.input_pin
          FROM    input_categories
          INNER
          JOIN    inputs ON input_categories.input_cat_id = inputs.input_cat_id
          WHERE   input_categories.input_cat_id = %d
        """ % int(cat_id))

        ci = []

        for data in db:
            if data[2]:
                cat_name = data[2]
            else:
                cat_name = data[1]

            c = {
                'input_cat_id': data[0],
                'input_pin': data[3],
                'input_cat_name': cat_name
            }

            ci.append(c)

        return ci
    
    @staticmethod
    def output_cats(cat_id):
        if cat_id == "null":
            return

        db.execute("""
          SELECT  output_categories.output_cat_id,
                  output_categories.output_cat_name,
                  output_categories.output_cat_alt_name,
                  outputs.output_pin
          FROM    output_categories
          INNER
          JOIN    outputs ON output_categories.output_cat_id = outputs.output_cat_id
          WHERE   output_categories.output_cat_id = %d
        """ % int(cat_id))

        ci = []

        for data in db:
            if data[2]:
                cat_name = data[2]
            else:
                cat_name = data[1]

            c = {
                'output_cat_id': data[0],
                'output_pin': data[3],
                'output_cat_name': cat_name
            }

            ci.append(c)

        return ci